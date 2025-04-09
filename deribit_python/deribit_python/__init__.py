"""
Deribit Python Wrapper

A Python wrapper for the Deribit cryptocurrency exchange API.
"""

from .client import DeribitClient
from .exceptions import (
    DeribitAPIError,
    DeribitAuthenticationError,
    DeribitRequestError,
    DeribitResponseError
)

__version__ = "0.1.0"
__all__ = [
    "DeribitClient",
    "DeribitAPIError",
    "DeribitAuthenticationError",
    "DeribitRequestError",
    "DeribitResponseError"
] 