"""
Utility functions for the Deribit Python wrapper.
"""
import hmac
import hashlib
import time
from typing import Dict

def generate_signature(api_secret: str, data: Dict) -> str:
    """
    Generate signature for API authentication.

    Args:
        api_secret (str): API secret key
        data (dict): Data to sign

    Returns:
        str: Generated signature
    """
    # Convert data to string and encode
    data_str = str(data)
    data_bytes = data_str.encode('utf-8')
    
    # Create HMAC using SHA256
    signature = hmac.new(
        api_secret.encode('utf-8'),
        data_bytes,
        hashlib.sha256
    ).hexdigest()
    
    return signature

def get_timestamp() -> int:
    """
    Get current timestamp in milliseconds.

    Returns:
        int: Current timestamp
    """
    return int(time.time() * 1000) 