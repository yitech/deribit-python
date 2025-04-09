"""
Tests for the JSON-RPC module.
"""
import json
import unittest
from unittest.mock import patch

from deribit_python.jsonrpc import JsonRpcRequest, JsonRpcResponse
from deribit_python.exceptions import DeribitAPIError


class TestJsonRpcRequest(unittest.TestCase):
    """Test the JsonRpcRequest class."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        request = JsonRpcRequest("test_method")
        self.assertEqual(request.method, "test_method")
        self.assertEqual(request.params, {})
        self.assertIsNotNone(request.request_id)

    def test_init_with_custom_values(self):
        """Test initialization with custom values."""
        request_id = "test-id-123"
        params = {"param1": "value1", "param2": 42}
        request = JsonRpcRequest("test_method", params, request_id)
        self.assertEqual(request.method, "test_method")
        self.assertEqual(request.params, params)
        self.assertEqual(request.request_id, request_id)

    def test_to_dict(self):
        """Test conversion to dictionary."""
        request_id = "test-id-123"
        params = {"param1": "value1", "param2": 42}
        request = JsonRpcRequest("test_method", params, request_id)
        request_dict = request.to_dict()
        
        self.assertEqual(request_dict["jsonrpc"], "2.0")
        self.assertEqual(request_dict["method"], "test_method")
        self.assertEqual(request_dict["params"], params)
        self.assertEqual(request_dict["id"], request_id)

    def test_to_json(self):
        """Test conversion to JSON string."""
        request_id = "test-id-123"
        params = {"param1": "value1", "param2": 42}
        request = JsonRpcRequest("test_method", params, request_id)
        json_str = request.to_json()
        
        # Parse the JSON string back to a dictionary
        json_dict = json.loads(json_str)
        self.assertEqual(json_dict["jsonrpc"], "2.0")
        self.assertEqual(json_dict["method"], "test_method")
        self.assertEqual(json_dict["params"], params)
        self.assertEqual(json_dict["id"], request_id)


class TestJsonRpcResponse(unittest.TestCase):
    """Test the JsonRpcResponse class."""

    def test_init_with_dict(self):
        """Test initialization with a dictionary."""
        response_data = {
            "jsonrpc": "2.0",
            "result": {"key": "value"},
            "id": "test-id-123",
            "testnet": True,
            "usIn": 1000,
            "usOut": 2000,
            "usDiff": 1000
        }
        response = JsonRpcResponse(response_data)
        self.assertEqual(response.data, response_data)

    def test_init_with_json_string(self):
        """Test initialization with a JSON string."""
        response_data = {
            "jsonrpc": "2.0",
            "result": {"key": "value"},
            "id": "test-id-123"
        }
        json_str = json.dumps(response_data)
        response = JsonRpcResponse(json_str)
        self.assertEqual(response.data, response_data)

    def test_result_property(self):
        """Test the result property."""
        response_data = {
            "jsonrpc": "2.0",
            "result": {"key": "value"},
            "id": "test-id-123"
        }
        response = JsonRpcResponse(response_data)
        self.assertEqual(response.result, {"key": "value"})

    def test_result_property_with_error(self):
        """Test the result property with an error response."""
        response_data = {
            "jsonrpc": "2.0",
            "error": {
                "code": 10001,
                "message": "Test error message"
            },
            "id": "test-id-123"
        }
        response = JsonRpcResponse(response_data)
        
        with self.assertRaises(DeribitAPIError) as context:
            _ = response.result
        
        self.assertIn("Test error message", str(context.exception))
        self.assertIn("10001", str(context.exception))

    def test_id_property(self):
        """Test the id property."""
        response_data = {
            "jsonrpc": "2.0",
            "result": {"key": "value"},
            "id": "test-id-123"
        }
        response = JsonRpcResponse(response_data)
        self.assertEqual(response.id, "test-id-123")

    def test_jsonrpc_property(self):
        """Test the jsonrpc property."""
        response_data = {
            "jsonrpc": "2.0",
            "result": {"key": "value"},
            "id": "test-id-123"
        }
        response = JsonRpcResponse(response_data)
        self.assertEqual(response.jsonrpc, "2.0")

    def test_testnet_property(self):
        """Test the testnet property."""
        response_data = {
            "jsonrpc": "2.0",
            "result": {"key": "value"},
            "id": "test-id-123",
            "testnet": True
        }
        response = JsonRpcResponse(response_data)
        self.assertTrue(response.testnet)
        
        response_data["testnet"] = False
        response = JsonRpcResponse(response_data)
        self.assertFalse(response.testnet)
        
        # Default value when testnet is not present
        del response_data["testnet"]
        response = JsonRpcResponse(response_data)
        self.assertFalse(response.testnet)

    def test_performance_metrics_property(self):
        """Test the performance_metrics property."""
        response_data = {
            "jsonrpc": "2.0",
            "result": {"key": "value"},
            "id": "test-id-123",
            "usIn": 1000,
            "usOut": 2000,
            "usDiff": 1000
        }
        response = JsonRpcResponse(response_data)
        metrics = response.performance_metrics
        
        self.assertEqual(metrics["usIn"], 1000)
        self.assertEqual(metrics["usOut"], 2000)
        self.assertEqual(metrics["usDiff"], 1000)
        
        # Default values when metrics are not present
        del response_data["usIn"]
        del response_data["usOut"]
        del response_data["usDiff"]
        response = JsonRpcResponse(response_data)
        metrics = response.performance_metrics
        
        self.assertEqual(metrics["usIn"], 0)
        self.assertEqual(metrics["usOut"], 0)
        self.assertEqual(metrics["usDiff"], 0)


if __name__ == "__main__":
    unittest.main() 