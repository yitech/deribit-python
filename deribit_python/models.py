from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List
import uuid
import json
from datetime import datetime


@dataclass
class OrderBookStats:
    """Statistics for the order book."""
    high: Optional[float] = None
    low: Optional[float] = None
    price_change: Optional[float] = None
    volume: float = 0.0
    volume_usd: float = 0.0
    volume_notional: float = 0.0


@dataclass
class OrderBookGreeks:
    """Option Greeks for the instrument."""
    delta: float = 0.0
    gamma: float = 0.0
    vega: float = 0.0
    theta: float = 0.0
    rho: float = 0.0


@dataclass
class OrderBookEntry:
    """Single entry in the order book (bid or ask)."""
    price: float
    amount: float


@dataclass
class OrderBook:
    """
    Represents the order book for an instrument.
    
    Attributes:
        timestamp: Unix timestamp in milliseconds
        state: State of the instrument (e.g., 'open', 'closed')
        stats: Trading statistics
        greeks: Option Greeks
        change_id: Order book change identifier
        index_price: Current index price
        instrument_name: Name of the instrument
        bids: List of bid orders [price, amount]
        asks: List of ask orders [price, amount]
        last_price: Last traded price
        min_price: Minimum price
        max_price: Maximum price
        open_interest: Open interest
        mark_price: Mark price
        best_ask_price: Best ask price
        best_bid_price: Best bid price
        interest_rate: Interest rate
        mark_iv: Mark implied volatility
        bid_iv: Bid implied volatility
        ask_iv: Ask implied volatility
        underlying_price: Price of the underlying asset
        underlying_index: Name of the underlying index
        estimated_delivery_price: Estimated delivery price
        best_ask_amount: Amount at best ask
        best_bid_amount: Amount at best bid
        delivery_price: Delivery price
    """
    timestamp: int
    state: str
    stats: OrderBookStats
    greeks: OrderBookGreeks
    change_id: int
    index_price: float
    instrument_name: str
    bids: List[OrderBookEntry]
    asks: List[OrderBookEntry]
    last_price: Optional[float]
    min_price: float
    max_price: float
    open_interest: float
    mark_price: float
    best_ask_price: float
    best_bid_price: float
    interest_rate: float
    mark_iv: float
    bid_iv: float
    ask_iv: float
    underlying_price: float
    underlying_index: str
    estimated_delivery_price: str
    best_ask_amount: float
    best_bid_amount: float
    delivery_price: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrderBook':
        """Create an OrderBook instance from a dictionary."""
        # Convert stats dictionary to OrderBookStats
        stats = OrderBookStats(**data.get('stats', {}))
        
        # Convert greeks dictionary to OrderBookGreeks
        greeks = OrderBookGreeks(**data.get('greeks', {}))
        
        # Convert bids and asks lists to OrderBookEntry objects
        bids = [OrderBookEntry(price=b[0], amount=b[1]) for b in data.get('bids', [])]
        asks = [OrderBookEntry(price=a[0], amount=a[1]) for a in data.get('asks', [])]
        
        # Create OrderBook instance with all fields
        return cls(
            timestamp=data['timestamp'],
            state=data['state'],
            stats=stats,
            greeks=greeks,
            change_id=data['change_id'],
            index_price=data['index_price'],
            instrument_name=data['instrument_name'],
            bids=bids,
            asks=asks,
            last_price=data['last_price'],
            min_price=data['min_price'],
            max_price=data['max_price'],
            open_interest=data['open_interest'],
            mark_price=data['mark_price'],
            best_ask_price=data['best_ask_price'],
            best_bid_price=data['best_bid_price'],
            interest_rate=data['interest_rate'],
            mark_iv=data['mark_iv'],
            bid_iv=data['bid_iv'],
            ask_iv=data['ask_iv'],
            underlying_price=data['underlying_price'],
            underlying_index=data['underlying_index'],
            estimated_delivery_price=data['estimated_delivery_price'],
            best_ask_amount=data['best_ask_amount'],
            best_bid_amount=data['best_bid_amount'],
            delivery_price=data['delivery_price']
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the OrderBook to a dictionary."""
        return {
            'timestamp': self.timestamp,
            'state': self.state,
            'stats': asdict(self.stats),
            'greeks': asdict(self.greeks),
            'change_id': self.change_id,
            'index_price': self.index_price,
            'instrument_name': self.instrument_name,
            'bids': [[b.price, b.amount] for b in self.bids],
            'asks': [[a.price, a.amount] for a in self.asks],
            'last_price': self.last_price,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'open_interest': self.open_interest,
            'mark_price': self.mark_price,
            'best_ask_price': self.best_ask_price,
            'best_bid_price': self.best_bid_price,
            'interest_rate': self.interest_rate,
            'mark_iv': self.mark_iv,
            'bid_iv': self.bid_iv,
            'ask_iv': self.ask_iv,
            'underlying_price': self.underlying_price,
            'underlying_index': self.underlying_index,
            'estimated_delivery_price': self.estimated_delivery_price,
            'best_ask_amount': self.best_ask_amount,
            'best_bid_amount': self.best_bid_amount,
            'delivery_price': self.delivery_price
        }

    @property
    def datetime(self) -> datetime:
        """Convert timestamp to datetime object."""
        return datetime.fromtimestamp(self.timestamp / 1000)  # Convert from milliseconds to seconds

@dataclass
class TickerStats:
    high: Optional[float] = None
    low: Optional[float] = None
    price_change: Optional[float] = None
    volume: Optional[float] = None
    volume_usd: Optional[float] = None
    volume_notional: Optional[float] = None


@dataclass
class Ticker:
    """
    Represents the ticker for an instrument.

    Attributes:
        timestamp: Unix timestamp in milliseconds
        best_ask_amount: Amount at best ask
        best_ask_price: Price at best ask
        best_bid_amount: Amount at best bid
        best_bid_price: Price at best bid
        current_funding: Current funding rate
        estimated_delivery_price: Estimated delivery price
        funding_8h: Funding rate in the last 8 hours
        index_price: Current index price
        instrument_name: Name of the instrument
        interest_value: Interest value
        last_price: Last traded price
        mark_price: Mark price
        max_price: Maximum price
        min_price: Minimum price
        open_interest: Open interest
        settlement_price: Settlement price
        state: State of the instrument
    """
    timestamp: int
    best_ask_amount: float
    best_ask_price: float
    best_bid_amount: float
    best_bid_price: float
    current_funding: Optional[float]
    estimated_delivery_price: float
    funding_8h: Optional[float]
    index_price: float
    instrument_name: str
    interest_value: Optional[float]
    last_price: float
    mark_price: float
    max_price: float
    min_price: float
    open_interest: float
    settlement_price: Optional[float]
    state: str
    stats: TickerStats

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Ticker':
        stats = TickerStats(**data.get('stats', {}))
        return cls(
            timestamp=data['timestamp'],
            best_ask_amount=data['best_ask_amount'],
            best_ask_price=data['best_ask_price'],
            best_bid_amount=data['best_bid_amount'],
            best_bid_price=data['best_bid_price'],
            current_funding=data.get('current_funding'),
            estimated_delivery_price=data['estimated_delivery_price'],
            funding_8h=data.get('funding_8h'),
            index_price=data['index_price'],
            instrument_name=data['instrument_name'],
            interest_value=data.get('interest_value'),
            last_price=data['last_price'],
            mark_price=data['mark_price'],
            max_price=data['max_price'],
            min_price=data['min_price'],
            open_interest=data['open_interest'],
            settlement_price=data['settlement_price'],
            state=data['state'],
            stats=stats
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp,
            'best_ask_amount': self.best_ask_amount,
            'best_ask_price': self.best_ask_price,
            'best_bid_amount': self.best_bid_amount,
            'best_bid_price': self.best_bid_price,
            'current_funding': self.current_funding,
            'estimated_delivery_price': self.estimated_delivery_price,
            'funding_8h': self.funding_8h,
            'index_price': self.index_price,
            'instrument_name': self.instrument_name,
            'interest_value': self.interest_value,
            'last_price': self.last_price,
            'mark_price': self.mark_price,
            'max_price': self.max_price,
            'min_price': self.min_price,
            'open_interest': self.open_interest,
            'settlement_price': self.settlement_price,
            'state': self.state,
            'stats': asdict(self.stats)
        }

    @property
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp / 1000)


@dataclass
class JsonRpcRequest:
    """
    JSON-RPC 2.0 request object.
    
    Attributes:
        method: The name of the method to be invoked
        params: The parameters for the method (optional)
        request_id: The request identifier (optional, defaults to a random UUID)
        jsonrpc: The JSON-RPC protocol version (defaults to "2.0")
    """
    method: str
    params: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None
    jsonrpc: str = "2.0"
    
    def __post_init__(self):
        """Initialize default values after instance creation."""
        if self.request_id is None:
            self.request_id = str(uuid.uuid4())
        if self.params is None:
            self.params = {}
            
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the request to a dictionary.
        
        Returns:
            Dict containing the JSON-RPC request
        """
        return {
            "jsonrpc": self.jsonrpc,
            "method": self.method,
            "params": self.params,
            "id": self.request_id
        }
        
    def to_json(self) -> str:
        """
        Convert the request to a JSON string.
        
        Returns:
            JSON string representation of the request
        """
        return json.dumps(self.to_dict())


@dataclass
class JsonRpcResponse:
    """
    JSON-RPC 2.0 response object.
    
    Attributes:
        result: The result of the method invocation (if successful)
        error: The error object (if the invocation failed)
        request_id: The request identifier
        jsonrpc: The JSON-RPC protocol version
        metadata: Additional metadata about the response (e.g., timing, headers)
    """
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None
    jsonrpc: str = "2.0"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JsonRpcResponse':
        """
        Create a JsonRpcResponse from a dictionary.
        
        Args:
            data: The dictionary containing the JSON-RPC response
            
        Returns:
            A new JsonRpcResponse instance
        """
        return cls(
            result=data.get("result"),
            error=data.get("error"),
            request_id=data.get("id"),
            jsonrpc=data.get("jsonrpc", "2.0"),
            metadata={k: v for k, v in data.items() if k not in ["result", "error", "id", "jsonrpc"]}
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'JsonRpcResponse':
        """
        Create a JsonRpcResponse from a JSON string.
        
        Args:
            json_str: The JSON string containing the JSON-RPC response
            
        Returns:
            A new JsonRpcResponse instance
        """
        return cls.from_dict(json.loads(json_str))
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the response to a dictionary.
        
        Returns:
            Dict containing the JSON-RPC response
        """
        data = {
            "jsonrpc": self.jsonrpc,
            "id": self.request_id
        }
        
        if self.error is not None:
            data["error"] = self.error
        else:
            data["result"] = self.result
            
        # Add metadata
        data.update(self.metadata)
        
        return data
    
    def to_json(self) -> str:
        """
        Convert the response to a JSON string.
        
        Returns:
            JSON string representation of the response
        """
        return json.dumps(self.to_dict())
    
    @property
    def is_error(self) -> bool:
        """
        Check if the response contains an error.
        
        Returns:
            True if the response contains an error, False otherwise
        """
        return self.error is not None
    
    @property
    def error_code(self) -> Optional[int]:
        """
        Get the error code from the response.
        
        Returns:
            The error code if the response contains an error, None otherwise
        """
        return self.error.get("code") if self.error else None
    
    @property
    def error_message(self) -> Optional[str]:
        """
        Get the error message from the response.
        
        Returns:
            The error message if the response contains an error, None otherwise
        """
        return self.error.get("message") if self.error else None