# src/main.py
import sys
import os
import json
import requests
import logging

# Add the project root directory to the system path
sys.path.append(os.path.abspath(path=os.path.join(os.path.dirname(p=__file__), '..')))
from config import Config
from signing import create_message, sign_message

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(filename=Config.log_file),
        logging.StreamHandler()  # Optional: also log to the console
    ]
)
logger = logging.getLogger(name=__name__)

def prepare_payload(transaction_details: dict, signature: str) -> str:
    """Prepare the payload with the signature added."""
    transaction_details["token"] = signature
    return json.dumps(obj=transaction_details)

def send_request(method: str, url: str, headers: dict, payload: str, auth: tuple[str, str]) -> requests.Response:
    """Send an HTTP request and return the response."""
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=payload,
            auth=auth
        )
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logger.error(msg=f"Request failed: {e}")
        raise

def main() -> None:
    try:
        # Create the message and sign it
        message: bytes = create_message(transaction_details=Config.transaction_details)
        signature: str = sign_message(
            message=message,
            pfx_password=Config.pfx_password,
            pfx_path=Config.pfx_path
        )
        
        # Prepare the payload with the signature added
        payload = prepare_payload(transaction_details=Config.transaction_details, 
                                  signature=signature)
        
        # Send the POST request
        response = send_request(
            method='POST',
            url=Config.url,
            headers=Config.headers,
            payload=payload,
            auth=Config.auth
        )

        print(json.dumps(obj=response.json(), indent=4))
        # Log the response for debugging
        logger.info(msg=f"Token: {response.status_code}")
        logger.info(msg=f"Response status code: {payload}")
        logger.info(msg=f"Response text: {response.text}")

    except Exception as e:
        logger.error(msg=f"An error occurred: {e}")

if __name__ == "__main__":
    main()
