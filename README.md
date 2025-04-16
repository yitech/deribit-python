# Deribit Python Client

A lightweight Python client for interacting with the [Deribit](https://docs.deribit.com/) cryptocurrency exchange API.

Supports:
- ✅ **Public HTTP (JSON-RPC)** methods (sync & async)
- 🚧 **Private HTTP** and **WebSocket Streaming API** (coming soon)

This module uses:
- HTTP requests (JSON-RPC over HTTP) for **synchronous** calls
- WebSocket (JSON-RPC over WebSocket) for **asynchronous** methods  
**➡️ We recommend using the async client for real-time data and better performance.**

---

## 🚀 Installation

Install via Git:

```bash
git clone https://github.com/yitech/deribit-python.git
cd deribit-python
pip install .
```
## 🧩 Synchronous Example

```python
from deribit_python.client import DeribitClient
import time

def main():
    api_key = ""
    api_secret = ""

    client = DeribitClient(api_key=api_key, api_secret=api_secret, testnet=True)

    instrument_name = "BTC-PERPETUAL"
    try:
        end_time = int(time.time() * 1000)
        start_time = end_time - 86400000  # 24 hours ago

        res = client.get_funding_rate_history(instrument_name, start_time, end_time)
        print("Funding Rate History:", res)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
```

## ⚡ Asynchronous Example (Recommended)

```python
import asyncio
from deribit_python.async_client import DeribitAsyncClient

async def main():
    api_key = ""
    api_secret = ""

    async with DeribitAsyncClient(api_key=api_key, api_secret=api_secret, testnet=False) as client:
        instrument_name = "BTC-PERPETUAL"
        try:
            ticker = await client.get_ticker(instrument_name)
            print("Ticker Information:")
            print(ticker)
        except Exception as e:
            print(f"An error occurred: {e}")

asyncio.run(main())
```

## 📌 Notes
The project is currently in active development.

✅ Basic public endpoints are implemented and tested.

🔜 Private account APIs and WebSocket streaming APIs are planned for upcoming versions.

Check the GitHub Repo for updates and contributions. 