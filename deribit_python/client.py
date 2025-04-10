"""
Deribit API Client

This module provides the main client class for interacting with the Deribit API.
"""
from typing import Dict, Optional, Union, Any, List
import requests
from .models import JsonRpcRequest, JsonRpcResponse
from .exceptions import DeribitAPIException
from .consts import DeribitMethod, TESTNET_BASE_URL, MAINNET_BASE_URL

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
        self.base_url = TESTNET_BASE_URL if testnet else MAINNET_BASE_URL
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            "Content-Type": "application/json",
        })
        
        if api_key and api_secret:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
            })

    def _make_request(self, method: str, params: Dict[str, Any]) -> Any:
        """
        Make a JSON-RPC request to the Deribit API.
        
        Args:
            method: The JSON-RPC method to call
            params: The parameters for the method
            
        Returns:
            The result from the API response
            
        Raises:
            DeribitAPIException: If the API request fails
        """
        request = JsonRpcRequest(
            method=method,
            params=params
        )
        
        try:
            response = self.session.post(
                self.base_url,
                json=request.to_dict()
            )
            response.raise_for_status()
            
            jsonrpc_response = JsonRpcResponse.from_dict(response.json())
            
            if jsonrpc_response.is_error:
                raise DeribitAPIException(
                    f"API Error: {jsonrpc_response.error_message} (code: {jsonrpc_response.error_code})"
                )
                
            return jsonrpc_response.result
            
        except requests.exceptions.RequestException as e:
            raise DeribitAPIException(f"Request failed: {str(e)}")
        except Exception as e:
            raise DeribitAPIException(f"Unexpected error: {str(e)}")

    def get_order_book(self, instrument_name: str, depth: int = 10) -> Dict[str, Any]:
        """
        Get the order book for a given instrument.
        
        Args:
            instrument_name: The name of the instrument
            depth: The depth of the order book (default: 10)
            
        Returns:
            The order book data
            
        Raises:
            DeribitAPIException: If the API request fails
        """
        return self._make_request(
            DeribitMethod.GET_ORDER_BOOK,
            {
                "instrument_name": instrument_name,
                "depth": depth
            }
        )
            

    