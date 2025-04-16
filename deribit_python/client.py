"""
Deribit API Client

This module provides the main client class for interacting with the Deribit API.
"""
from typing import Dict, Optional, Union, Any, List
import requests
from .models import (
    JsonRpcRequest, JsonRpcResponse, 
    OrderBook, Ticker, Instrument, BookSummary, ContractSize, Currency, DeliveryPriceResponse,
    FundingChartData
)
from .exceptions import DeribitAPIException, raise_deribit_exception
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
                raise_deribit_exception(
                    jsonrpc_response.error_code,
                    jsonrpc_response.error_message
                )
            return jsonrpc_response.result
            
        except requests.exceptions.RequestException as e:
            raise DeribitAPIException(f"Request failed: {str(e)}")
        except Exception as e:
            raise DeribitAPIException(f"Unexpected error: {str(e)}")
        
    def get_instruments(self, currency: str = "any", kind: str = None, expire: bool = False) -> List[Instrument]:
        params = {"currency": currency}
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
    
    def get_book_summary_by_currency(self, currency: str, kind: Optional[str]) -> List[BookSummary]:
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
    
    def get_book_summary_by_instrument(self, instrument_name: str) -> List[BookSummary]:
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
    
    def get_currencies(self) -> List[Currency]:
        """
        Get the list of available currencies.
        
        Returns:
            List of available currencies
            
        Raises:
            DeribitAPIException: If the API request fails
        """
        result = self._make_request(
            DeribitMethod.GET_CURRENCIES,
            {}
        )
        return [Currency.from_dict(item) for item in result]
    
    def get_delivery_prices(self, index_name: str, offset: Optional[int] = None, count: Optional[int] = None) -> DeliveryPriceResponse:
        """
        Get the delivery prices for a given instrument.
        
        Args:
            instrument_name: The name of the instrument
            
        Returns:
            List of delivery prices for the given instrument
            
        Raises:
            DeribitAPIException: If the API request fails
        """
        params = {
            "index_name": index_name
        }
        if offset is not None:
            params["offset"] = offset
        if count is not None:
            params["count"] = count
        result = self._make_request(
            DeribitMethod.GET_DELIVERY_PRICES,
            params
        )
        return DeliveryPriceResponse.from_dict(result)
    
    def get_expirations(self, currency: str = "any", kind: str = "any") -> List[Dict[str, Any]]:
        """
        Get the list of expirations for a given currency and kind.
        
        Args:
            currency: The currency to get expirations for
            kind: The kind of instruments to include
            
        Returns:
            List of expirations for the given currency and kind
            
        Raises:
            DeribitAPIException: If the API request fails
        """
        params = {
            "currency": currency,
            "kind": kind
        }
        result = self._make_request(
            DeribitMethod.GET_EXPIRATIONS,
            params
        )
        return result
    
    def get_funding_chart_data(self, instrument_name: str, length: str) -> FundingChartData:
        """
        Get the funding chart data for a given instrument.
        
        Args:
            instrument_name: The name of the instrument
            start_timestamp: The start timestamp for the data (optional)
            end_timestamp: The end timestamp for the data (optional)
            
        Returns:
            List of funding chart data for the given instrument
            
        Raises:
            DeribitAPIException: If the API request fails
        """
        params = {
            "instrument_name": instrument_name,
            "length": length
        }
        result = self._make_request(
            DeribitMethod.GET_FUNDING_CHART_DATA,
            params
        )
        return FundingChartData.from_dict(result)
            

    