# Deribit Python Wrapper

A Python wrapper for the Deribit cryptocurrency exchange API. This library provides a simple and intuitive interface to interact with Deribit's trading platform.

## Features

- REST API integration
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

# Place a limit order
order = client.create_order(
    instrument_name="BTC-PERPETUAL",
    side="buy",
    amount=0.1,
    price=50000,
    type="limit"
)
```

## Documentation

For detailed documentation, please visit [documentation link].

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.