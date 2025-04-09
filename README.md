# Deribit Python Wrapper

A Python wrapper for the Deribit cryptocurrency exchange API. This library provides a simple and intuitive interface to interact with Deribit's trading platform.

## Features

- REST API integration
- JSON-RPC support for both HTTP and WebSocket
- WebSocket support for real-time data
- Support for both testnet and mainnet
- Comprehensive error handling
- Type hints for better IDE support
- Async/await support for modern Python applications

## Installation

```bash
pip install deribit-python
```

## Quick Start

```python
from deribit import DeribitClient

# Initialize the client (testnet)
client = DeribitClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
    testnet=True
)

# Get BTC-PERPETUAL ticker
ticker = client.get_ticker("BTC-PERPETUAL")
print(f"Current BTC price: {ticker['last_price']}")

# Get order book for an option
order_book = client.get_order_book(
    instrument_name="BNB_USDC-10APR25-490-P",
    depth=10
)
print(f"Best bid price: {order_book['best_bid_price']}")
print(f"Best ask price: {order_book['best_ask_price']}")

# Place a limit order
order = client.create_order(
    instrument_name="BTC-PERPETUAL",
    side="buy",
    amount=0.1,
    price=50000,
    type="limit"
)
```

## JSON-RPC Support

This library supports both HTTP and WebSocket JSON-RPC methods. The JSON-RPC functionality is handled automatically by the client, but you can also use the JSON-RPC classes directly if needed:

```python
from deribit import JsonRpcRequest, JsonRpcResponse

# Create a JSON-RPC request
request = JsonRpcRequest(
    method="get_order_book",
    params={
        "instrument_name": "BTC-PERPETUAL",
        "depth": 10
    }
)

# Convert to JSON
json_request = request.to_json()
print(json_request)

# Parse a JSON-RPC response
response_data = {
    "jsonrpc": "2.0",
    "result": {
        "timestamp": 1744208208919,
        "state": "open",
        "bids": [],
        "asks": []
    },
    "id": "123",
    "testnet": True
}
response = JsonRpcResponse(response_data)
print(response.result)
```

## Documentation

For detailed documentation, please visit [documentation link].

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.