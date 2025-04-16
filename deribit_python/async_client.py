from typing import Dict, Optional, Union, Any, List
import asyncio
import websockets
import json
from .models import (
    JsonRpcRequest, JsonRpcResponse, 
    OrderBook, Ticker, Instrument, BookSummary, ContractSize, Currency, DeliveryPriceResponse,
    FundingChartData
)
from .exceptions import DeribitAPIException, raise_deribit_exception
from .consts import DeribitMethod, TESTNET_WS_URL, MAINNET_WS_URL


class DeribitAsyncClient:
    def __init__(self,
        api_key: str = "",
        api_secret: str = "",
        testnet: bool = True
    ):
        self.websocket = None
        self.pending_requests = {}
        self.pending_requests_lock = asyncio.Lock()  # Add a lock for thread-safe pending_requests
        self.url = TESTNET_WS_URL if testnet else MAINNET_WS_URL

    async def __aenter__(self):
        self.websocket = await websockets.connect(self.url)
        # Start a background task to handle incoming messages
        self.listener_task = asyncio.create_task(self._listen())
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.websocket:
            await self.websocket.close()
        # Cancel the listener task
        self.listener_task.cancel()
        try:
            await self.listener_task
        except asyncio.CancelledError:
            pass

    async def close(self):
        """Close the WebSocket connection and cancel the listener task."""
        if self.websocket:
            await self.websocket.close()
        if hasattr(self, 'listener_task') and self.listener_task:
            self.listener_task.cancel()
            try:
                await self.listener_task
            except asyncio.CancelledError:
                pass

    @classmethod
    async def create(cls, api_key: Optional[str] = None,
                    api_secret: Optional[str] = None,
                    testnet: bool = True):
        """Async class method to create and return an instance of DeribitAsyncClient."""
        instance = cls(api_key, api_secret, testnet)
        instance.websocket = await websockets.connect(instance.url)
        # Start a background task to handle incoming messages
        instance.listener_task = asyncio.create_task(instance._listen())
        return instance

    async def _listen(self):
        """Background task to listen for incoming messages."""
        try:
            while True:
                message = await self.websocket.recv()
                response = json.loads(message)
                message_id = response.get("id")
                if message_id in self.pending_requests:
                    # Set the result for the corresponding Future
                    self.pending_requests[message_id].set_result(response)
                    del self.pending_requests[message_id]
        except websockets.ConnectionClosed:
            pass

    async def _make_request(self, method: str, params: Dict[str, Any]) -> JsonRpcResponse:
        if not self.websocket:
            raise RuntimeError("WebSocket connection is not open. Use the async context manager.")

        msg = JsonRpcRequest(
            method=method,
            params=params,
        )

        # Create a Future to wait for the response
        future = asyncio.get_event_loop().create_future()
        async with self.pending_requests_lock:
            self.pending_requests[msg.request_id] = future

        # Send the request
        await self.websocket.send(msg.to_json())

        # Wait for the response
        response = await future
        jsonrpc_response = JsonRpcResponse.from_dict(response)
        if jsonrpc_response.is_error:
            raise_deribit_exception(
                jsonrpc_response.error_code,
                jsonrpc_response.error_message
            )
        return jsonrpc_response.result
    
    async def get_instruments(self, currency: str = "any", kind: str = None, expire: bool = False) -> List[Instrument]:
        params = {"currency": currency}
        if kind is not None:
            params.update({"kind": kind})
        params.update({"expire": expire})
        result = await self._make_request(
            DeribitMethod.GET_INSTRUMENTS,
            params
        )
        return [Instrument.from_dict(item) for item in result]
    
    async def get_ticker(self, instrument_name: str) -> Ticker:
        """
        Get the ticker for a given instrument.
        
        Args:
            instrument_name: The name of the instrument
        """
        result = await self._make_request(
            DeribitMethod.GET_TICKER,
            {
                "instrument_name": instrument_name
            }
        )
        return Ticker.from_dict(result)
    
    async def get_order_book(self, instrument_name: str, depth: int = 10) -> OrderBook:
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
    
    async def get_book_summary_by_currency(self, currency: str, kind: Optional[str]) -> List[BookSummary]:
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
    
    async def get_book_summary_by_instrument(self, instrument_name: str) -> List[BookSummary]:
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
    
    async def get_contract_size(self, instrument_name: str) -> float:
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
    
    async def get_currencies(self) -> List[Currency]:
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
    
    async def get_delivery_prices(self, index_name: str, offset: Optional[int] = None, count: Optional[int] = None) -> DeliveryPriceResponse:
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
    
    async def get_expirations(self, currency: str = "any", kind: str = "any") -> List[Dict[str, Any]]:
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
    
    async def get_funding_chart_data(self, instrument_name: str, length: str) -> FundingChartData:
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
    
