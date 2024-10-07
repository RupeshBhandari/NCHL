import base64
import logging
from OpenSSL import crypto
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(Config.log_file),
        logging.StreamHandler()  # Optional: also log to the console
    ]
)
logger = logging.getLogger(__name__)

def create_message(transaction_details: dict[str, str]) -> bytes:
    """
    Create a message string by concatenating transaction details in 'KEY=VALUE' format.
    
    Args:
    transaction_details (dict): A dictionary containing transaction details.
    
    Returns:
    bytes: The encoded message string in bytes.
    """
    try:
        # Create the message string by joining key-value pairs as "KEY=VALUE"
        message = ",".join(f"{key.upper()}={value}" for key, value in transaction_details.items())
        logger.info(f"Message: {message}")
        # Encode the message to bytes using UTF-8
        return message.encode('utf-8')
    except Exception as e:
        logger.error(f"Error creating message: {e}")
        raise

def sign_message(message: bytes, pfx_path: str, pfx_password: bytes) -> str:
    """
    Sign a message using the private key from a PKCS#12 (.pfx) file.
    
    Args:
    message (bytes): The message to be signed.
    pfx_path (str): The path to the PKCS#12 (.pfx) file.
    pfx_password (str): The password for the PKCS#12 file.
    
    Returns:
    str: The signature of the message, encoded in Base64.
    """
    try:
        # Open and read the PKCS#12 file
        with open(pfx_path, "rb") as key_file:
            pfx_data = key_file.read()
        
        # Load the private key from the PKCS#12 file
        p12 = crypto.load_pkcs12(pfx_data, pfx_password)
        pkey = p12.get_privatekey()
        
        # Sign the message using the private key and SHA-256 algorithm
        signature = crypto.sign(pkey, message, "sha256")
        logger.info(f"Signature: {base64.b64encode(signature).decode('utf-8')}")
        
        # Encode the signature to Base64 and return it
        return base64.b64encode(signature).decode('utf-8')
    except crypto.Error as e:
        logger.error(f"OpenSSL error: {e}")
        raise
    except FileNotFoundError:
        logger.error(f"File not found: {pfx_path}")
        raise
    except Exception as e:
        logger.error(f"Error signing message: {e}")
        raise
