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