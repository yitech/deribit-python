"""
Deribit API Client

This module provides the main client class for interacting with the Deribit API.
"""
from typing import Dict, Optional, Union
import requests
from .exceptions import DeribitAPIError
from .utils import generate_signature

class DeribitClient:
    """
    Main client class for interacting with the Deribit API.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        testnet: bool = True
    ):
        """
        Initialize the Deribit client.

        Args:
            api_key (str, optional): Your Deribit API key
            api_secret (str, optional): Your Deribit API secret
            testnet (bool): Whether to use testnet (default: True)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.base_url = "https://test.deribit.com" if testnet else "https://www.deribit.com"
        self.session = requests.Session()
        
        if api_key and api_secret:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
            })

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Dict:
        """
        Make a request to the Deribit API.

        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            params (dict, optional): Query parameters
            data (dict, optional): Request body data

        Returns:
            dict: API response

        Raises:
            DeribitAPIError: If the API request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise DeribitAPIError(f"API request failed: {str(e)}")

    def get_ticker(self, instrument_name: str) -> Dict:
        """
        Get ticker information for an instrument.

        Args:
            instrument_name (str): Instrument name (e.g., "BTC-PERPETUAL")

        Returns:
            dict: Ticker information
        """
        return self._request(
            method="GET",
            endpoint="/api/v2/public/get_ticker",
            params={"instrument_name": instrument_name}
        )

    def create_order(
        self,
        instrument_name: str,
        side: str,
        amount: float,
        price: Optional[float] = None,
        type: str = "limit"
    ) -> Dict:
        """
        Create a new order.

        Args:
            instrument_name (str): Instrument name (e.g., "BTC-PERPETUAL")
            side (str): Order side ("buy" or "sell")
            amount (float): Order amount
            price (float, optional): Order price (required for limit orders)
            type (str): Order type ("limit" or "market")

        Returns:
            dict: Order information
        """
        if not self.api_key or not self.api_secret:
            raise DeribitAPIError("API key and secret are required for trading")

        data = {
            "instrument_name": instrument_name,
            "side": side,
            "amount": amount,
            "type": type
        }
        
        if type == "limit" and price is not None:
            data["price"] = price

        return self._request(
            method="POST",
            endpoint="/api/v2/private/buy" if side == "buy" else "/api/v2/private/sell",
            data=data
        ) 