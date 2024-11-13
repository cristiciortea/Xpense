from datetime import datetime


def round_to_two_decimals(value: str) -> str:
    # Convert the string to a float
    number = float(value)

    # Round to 2 decimal places
    rounded_number = round(number, 2)

    # Format the number back to a string with 2 decimal places
    return f"{rounded_number:.2f}"


def human_readable_datetime(dt: datetime, only_date: bool = False) -> str:
    if only_date:
        # Format for only the date
        return dt.strftime("%B %d, %Y")  # e.g., "November 13, 2024"
    else:
        # Format for date and time
        return dt.strftime("%B %d, %Y %I:%M %p")  # e.g., "November 13, 2024 09:30 PM"
