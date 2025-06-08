import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# MSC API URL
url = os.getenv("MSC_TRACKING_URL")

# Headers loaded from env
headers = {
    "accept": os.getenv("MSC_HEADER_ACCEPT"),
    "accept-language": os.getenv("MSC_HEADER_ACCEPT_LANGUAGE"),
    "content-type": os.getenv("MSC_HEADER_CONTENT_TYPE"),
    "origin": os.getenv("MSC_HEADER_ORIGIN"),
    "referer": os.getenv("MSC_HEADER_REFERER"),
    "x-requested-with": os.getenv("MSC_HEADER_X_REQUESTED_WITH"),
}