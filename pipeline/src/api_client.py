import requests
from src.config import url, headers

def fetch_tracking_info(tracking_number: str, tracking_mode: str = "0") -> dict:
    payload = {"trackingNumber": tracking_number, "trackingMode": tracking_mode}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raises HTTPError if not 200

    data = response.json()
    if data.get("IsSuccess") is True and isinstance(data.get("Data"), dict):
        return data
    else:
        raise ValueError("No valid data returned from API.")