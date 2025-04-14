"""
Deribit API Client

This module provides the main client class for interacting with the Deribit API.
"""
from typing import Dict, Optional, Union, Any, List
import requests
from .models import (
    JsonRpcRequest, JsonRpcResponse, 
    OrderBook, Ticker, Instrument, BookSummary, ContractSize
)
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
        
    def get_instruments(self, instrument_name: Optional[str] = None, kind: str = None, expire: bool = True) -> List[Dict[str, Any]]:
        params = {}
        if instrument_name is None:
            params.update({"instrument_name": instrument_name})
        else:
            params = {"instrument_name": instrument_name}
        if kind is not None:
            params.update({"kind": kind})
        params.update({"expire": expire})
        result = self._make_request(
            DeribitMethod.GET_INSTRUMENTS,
            params
        )
        return [Instrument.from_dict(item) for item in result]
        
    def get_ticker(self, instrument_name: str) -> Ticker:
        """
        Get the ticker for a given instrument.
        
        Args:
            instrument_name: The name of the instrument
        """
        result = self._make_request(
            DeribitMethod.GET_TICKER,
            {
                "instrument_name": instrument_name
            }
        )
        print(result)
        return Ticker.from_dict(result)

    def get_order_book(self, instrument_name: str, depth: int = 10) -> OrderBook:
        """
        Get the order book for a given instrument.
        
        Args:
            instrument_name: The name of the instrument
            depth: The depth of the order book (default: 10)
            
        Returns:
            OrderBook instance containing the order book data
            
        Raises:
            DeribitAPIException: If the API request fails
        """
        result = self._make_request(
            DeribitMethod.GET_ORDER_BOOK,
            {
                "instrument_name": instrument_name,
                "depth": depth
            }
        )
        return OrderBook.from_dict(result)
    
    def get_book_summary_by_currency(self, currency: str, kind: Optional[str]) -> List[Dict[str, Any]]:
        """
        Get the book summary by currency.
        
        Args:
            currency: The currency to get the book summary for
            kind: The kind of instruments to include (optional)
            
        Returns:
            List of book summaries for the given currency
            
        Raises:
            DeribitAPIException: If the API request fails
        """
        params = {"currency": currency}
        if kind is not None:
            params["kind"] = kind
        result = self._make_request(
            DeribitMethod.GET_BOOK_SUMMARY_BY_CURRENCY,
            params
        )
        return [BookSummary.from_dict(item) for item in result]
    
    def get_book_summary_by_instrument(self, instrument_name: str) -> List[Dict[str, Any]]:
        """
        Get the book summary by instrument.
        
        Args:
            instrument_name: The name of the instrument
            
        Returns:
            List of book summaries for the given instrument
            
        Raises:
            DeribitAPIException: If the API request fails
        """
        result = self._make_request(
            DeribitMethod.GET_BOOK_SUMMARY_BY_INSTRUMENT,
            {
                "instrument_name": instrument_name
            }
        )
        return [BookSummary.from_dict(item) for item in result]
    
    def get_contract_size(self, instrument_name: str) -> float:
        """
        Get the contract size for a given instrument.
        
        Args:
            instrument_name: The name of the instrument
            
        Returns:
            The contract size for the given instrument
            
        Raises:
            DeribitAPIException: If the API request fails
        """
        result = self._make_request(
            DeribitMethod.GET_CONTRACT_SIZE,
            {
                "instrument_name": instrument_name
            }
        )
        return ContractSize.from_dict(result)
            

    