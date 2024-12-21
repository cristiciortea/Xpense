import base64
import hashlib
import os
import uuid
from datetime import datetime, timedelta

import requests
from fastapi import HTTPException


def register_as_oauth_client():
    url = "https://api.apistorebt.ro/bt/sb/oauth/register"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Request-ID": str(uuid.uuid4())
    }
    data = {
        "redirect_uris": ["https://localhost:8000/callback"],
        "client_name": "Xpense"
    }

    response = requests.post(url, headers=headers, json=data)
    register_info = response.json()
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail=register_info)

    return register_info


def initiate_user_consent():
    valid_until_date = (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')
    ip_response = requests.get('https://api.ipify.org?format=json')
    your_ip_address = ip_response.json()['ip']

    url = "https://api.apistorebt.ro/bt/sb/bt-psd2-aisp/v2/consents"
    headers = {
        "Content-Type": "application/json",
        "PSU-IP-Address": your_ip_address,
        "X-Request-ID": str(uuid.uuid4())
    }
    data = {
        "access": {"availableAccounts": "allAccounts"},
        "recurringIndicator": True,
        "validUntil": valid_until_date,
        "combinedServiceIndicator": False,
        "frequencyPerDay": 4
    }

    response = requests.post(url, headers=headers, json=data)
    consent_info = response.json()
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail=consent_info)

    return consent_info


def generate_code_verifier_and_challenge():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8').rstrip('=')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode(
        'utf-8').rstrip('=')
    return code_verifier, code_challenge
