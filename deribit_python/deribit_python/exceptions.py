"""
Custom exceptions for the Deribit Python wrapper.
"""

class DeribitAPIError(Exception):
    """Base exception for Deribit API errors."""
    pass

class DeribitAuthenticationError(DeribitAPIError):
    """Exception raised for authentication errors."""
    pass

class DeribitRequestError(DeribitAPIError):
    """Exception raised for request errors."""
    pass

class DeribitResponseError(DeribitAPIError):
    """Exception raised for response errors."""
    pass 