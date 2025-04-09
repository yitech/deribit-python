"""
Tests for the Deribit client module.
"""
import unittest
from unittest.mock import patch, MagicMock

from deribit_python.client import DeribitClient
from deribit_python.exceptions import DeribitAPIError
from deribit_python.jsonrpc import JsonRpcResponse


class TestDeribitClient(unittest.TestCase):
    """Test the DeribitClient class."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = DeribitClient(testnet=True)
        self.client_with_auth = DeribitClient(
            api_key="test_api_key",
            api_secret="test_api_secret",
            testnet=True
        )

    def test_init_with_testnet(self):
        """Test initialization with testnet."""
        client = DeribitClient(testnet=True)
        self.assertTrue(client.testnet)
        self.assertEqual(client.base_url, "https://test.deribit.com")
        
        client = DeribitClient(testnet=False)
        self.assertFalse(client.testnet)
        self.assertEqual(client.base_url, "https://www.deribit.com")

    def test_init_with_auth(self):
        """Test initialization with authentication."""
        client = DeribitClient(
            api_key="test_api_key",
            api_secret="test_api_secret",
            testnet=True
        )
        self.assertEqual(client.api_key, "test_api_key")
        self.assertEqual(client.api_secret, "test_api_secret")
        self.assertEqual(
            client.session.headers["Authorization"],
            "Bearer test_api_key"
        )

    @patch("requests.Session.request")
    def test_request(self, mock_request):
        """Test the _request method."""
        # Set up the mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "success"}
        mock_request.return_value = mock_response
        
        # Call the method
        result = self.client._request(
            method="GET",
            endpoint="/test",
            params={"param": "value"}
        )
        
        # Check the result
        self.assertEqual(result, {"result": "success"})
        
        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "GET")
        self.assertEqual(args[1], "https://test.deribit.com/test")
        self.assertEqual(kwargs["params"], {"param": "value"})

    @patch("requests.Session.request")
    def test_request_with_error(self, mock_request):
        """Test the _request method with an error."""
        # Set up the mock to raise an exception
        mock_request.side_effect = Exception("Test error")
        
        # Call the method and check that it raises the expected exception
        with self.assertRaises(DeribitAPIError) as context:
            self.client._request(method="GET", endpoint="/test")
        
        self.assertIn("Test error", str(context.exception))

    @patch("requests.Session.post")
    def test_jsonrpc_request(self, mock_post):
        """Test the _jsonrpc_request method."""
        # Set up the mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "result": {"key": "value"},
            "id": "test-id-123"
        }
        mock_post.return_value = mock_response
        
        # Call the method
        response = self.client._jsonrpc_request(
            method="test_method",
            params={"param": "value"}
        )
        
        # Check that the response is a JsonRpcResponse
        self.assertIsInstance(response, JsonRpcResponse)
        self.assertEqual(response.result, {"key": "value"})
        
        # Check that the request was made correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://test.deribit.com/api/v2/public/test_method")
        
        # Check the request body
        request_body = kwargs["json"]
        self.assertEqual(request_body["jsonrpc"], "2.0")
        self.assertEqual(request_body["method"], "test_method")
        self.assertEqual(request_body["params"], {"param": "value"})

    @patch("requests.Session.post")
    def test_jsonrpc_request_with_error(self, mock_post):
        """Test the _jsonrpc_request method with an error."""
        # Set up the mock to raise an exception
        mock_post.side_effect = Exception("Test error")
        
        # Call the method and check that it raises the expected exception
        with self.assertRaises(DeribitAPIError) as context:
            self.client._jsonrpc_request(method="test_method")
        
        self.assertIn("Test error", str(context.exception))

    @patch("deribit_python.client.DeribitClient._request")
    def test_get_ticker(self, mock_request):
        """Test the get_ticker method."""
        # Set up the mock response
        mock_request.return_value = {"last_price": 50000}
        
        # Call the method
        result = self.client.get_ticker("BTC-PERPETUAL")
        
        # Check the result
        self.assertEqual(result, {"last_price": 50000})
        
        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "GET")
        self.assertEqual(args[1], "/api/v2/public/get_ticker")
        self.assertEqual(kwargs["params"], {"instrument_name": "BTC-PERPETUAL"})

    @patch("deribit_python.client.DeribitClient._jsonrpc_request")
    def test_get_order_book(self, mock_jsonrpc_request):
        """Test the get_order_book method."""
        # Set up the mock response
        mock_response = MagicMock()
        mock_response.result = {
            "timestamp": 1744208208919,
            "state": "open",
            "bids": [[50000, 1.0], [49900, 2.0]],
            "asks": [[50100, 1.5], [50200, 3.0]],
            "best_bid_price": 50000,
            "best_ask_price": 50100
        }
        mock_jsonrpc_request.return_value = mock_response
        
        # Call the method
        result = self.client.get_order_book(
            instrument_name="BNB_USDC-10APR25-490-P",
            depth=5
        )
        
        # Check the result
        self.assertEqual(result["best_bid_price"], 50000)
        self.assertEqual(result["best_ask_price"], 50100)
        self.assertEqual(len(result["bids"]), 2)
        self.assertEqual(len(result["asks"]), 2)
        
        # Check that the request was made correctly
        mock_jsonrpc_request.assert_called_once()
        args, kwargs = mock_jsonrpc_request.call_args
        self.assertEqual(args[0], "get_order_book")
        self.assertEqual(
            kwargs["params"],
            {
                "instrument_name": "BNB_USDC-10APR25-490-P",
                "depth": 5
            }
        )

    @patch("deribit_python.client.DeribitClient._request")
    def test_create_order_without_auth(self, mock_request):
        """Test the create_order method without authentication."""
        # Call the method and check that it raises the expected exception
        with self.assertRaises(DeribitAPIError) as context:
            self.client.create_order(
                instrument_name="BTC-PERPETUAL",
                side="buy",
                amount=0.1,
                price=50000
            )
        
        self.assertIn("API key and secret are required", str(context.exception))
        
        # Check that the request was not made
        mock_request.assert_not_called()

    @patch("deribit_python.client.DeribitClient._request")
    def test_create_order_with_auth(self, mock_request):
        """Test the create_order method with authentication."""
        # Set up the mock response
        mock_request.return_value = {"order_id": "test-order-id"}
        
        # Call the method
        result = self.client_with_auth.create_order(
            instrument_name="BTC-PERPETUAL",
            side="buy",
            amount=0.1,
            price=50000
        )
        
        # Check the result
        self.assertEqual(result, {"order_id": "test-order-id"})
        
        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/api/v2/private/buy")
        
        # Check the request body
        request_body = kwargs["data"]
        self.assertEqual(request_body["instrument_name"], "BTC-PERPETUAL")
        self.assertEqual(request_body["side"], "buy")
        self.assertEqual(request_body["amount"], 0.1)
        self.assertEqual(request_body["price"], 50000)
        self.assertEqual(request_body["type"], "limit")


if __name__ == "__main__":
    unittest.main() 