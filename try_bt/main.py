import os
import pathlib
import uuid
from datetime import datetime
from typing import Optional

import requests
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from try_bt.register import register_as_oauth_client, initiate_user_consent, generate_code_verifier_and_challenge

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for client, consent, and token information
client_info = register_as_oauth_client()
consent_info = initiate_user_consent()
code_verifier, code_challenge = generate_code_verifier_and_challenge()
access_token = None


def get_redirect_response() -> RedirectResponse:
    if not client_info or not consent_info:
        raise HTTPException(status_code=400, detail="Client registration or consent initiation required")

    redirect_uri = "https://localhost:8000/callback"
    consent_id = consent_info.get("consentId")
    client_id = client_info.get("client_id")

    redirect_url = (
        f"https://apistorebt.ro/auth/realms/psd2-sb/protocol/openid-connect/auth?"
        f"client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope=AIS:{consent_id}"
        f"&state=state123test"
        f"&nonce=nonce123test"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )
    # return RedirectResponse(url=redirect_url)
    return redirect_url


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/callback")
async def callback(request: Request):
    global access_token
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    url = "https://api.apistorebt.ro/bt/sb/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "https://localhost:8000/callback",
        "client_id": client_info.get("client_id"),
        "client_secret": client_info.get("client_secret"),
        "code_verifier": code_verifier
    }

    response = requests.post(url, headers=headers, data=data)
    token_response = response.json()
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=token_response)

    access_token = token_response.get("access_token")
    return token_response


@app.get("/transactions")
async def get_bt_transactions(
        account_id: str = Query(..., description="The ID of the account to fetch transactions for"),
        date_from: str = Query(...,
                               description="Starting date (inclusive) of the transaction list in YYYY-MM-DD format"),
        date_to: Optional[str] = Query(None,
                                       description="End date (inclusive) of the transaction list in YYYY-MM-DD format"),
        booking_status: Optional[str] = Query("both", enum=["booked", "pending", "both"],
                                              description="The booking status of the transactions")
):
    if not access_token:
        return get_redirect_response()

    # Default date_to to today's date if not provided
    if not date_to:
        date_to = datetime.now().strftime("%Y-%m-%d")

    # Construct the query parameters
    params = {
        "bookingStatus": booking_status,
        "dateFrom": date_from,
        "dateTo": date_to
    }

    # Example API call to get transactions using the access token and account ID
    url = f"https://api.apistorebt.ro/bt/sb/bt-psd2-aisp/v2/accounts/{account_id}/transactions"
    consent_id = consent_info.get("consentId")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Consent-ID": consent_id,
        "X-Request-ID": str(uuid.uuid4()),
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@app.get("/accounts")
async def get_accounts():
    if not access_token:
        return get_redirect_response()

    url = "https://api.apistorebt.ro/bt/sb/bt-psd2-aisp/v2/accounts"

    consent_id = consent_info.get("consentId")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Consent-ID": consent_id,
        "X-Request-ID": str(uuid.uuid4()),
        "accept": "application/json",  # optional.
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    accounts_response = response.json()
    return accounts_response


if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # Adjust this path as needed
        host=os.environ.get("SERVICE_HOST", "0.0.0.0"),
        port=int(os.environ.get("SERVICE_PORT", 8000)),
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem",
        log_level="info",
        reload=bool(os.environ.get("ENABLE_CONTAINER_RELOAD", False)),
        reload_dirs=[pathlib.Path(__file__).parent.as_posix()],
        use_colors=True,
    )
