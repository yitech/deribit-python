"""
JSON-RPC handling for Deribit API.
"""
import json
import uuid
from typing import Any, Dict, Optional, Union

class JsonRpcRequest:
    """
    JSON-RPC request builder.
    """
    
    def __init__(
        self,
        method: str,
        params: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None
    ):
        """
        Initialize a JSON-RPC request.
        
        Args:
            method: The JSON-RPC method to call
            params: Parameters for the method
            request_id: Optional request ID (defaults to a random UUID)
        """
        self.method = method
        self.params = params or {}
        self.request_id = request_id or str(uuid.uuid4())
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the request to a dictionary.
        
        Returns:
            Dict containing the JSON-RPC request
        """
        return {
            "jsonrpc": "2.0",
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


class JsonRpcResponse:
    """
    JSON-RPC response parser.
    """
    
    def __init__(self, response_data: Union[str, Dict[str, Any]]):
        """
        Initialize a JSON-RPC response parser.
        
        Args:
            response_data: The response data as a string or dictionary
        """
        if isinstance(response_data, str):
            self.data = json.loads(response_data)
        else:
            self.data = response_data
            
    @property
    def result(self) -> Any:
        """
        Get the result from the response.
        
        Returns:
            The result data
            
        Raises:
            DeribitAPIError: If the response contains an error
        """
        if "error" in self.data:
            from .exceptions import DeribitAPIError
            error = self.data["error"]
            raise DeribitAPIError(
                f"JSON-RPC error: {error.get('message', 'Unknown error')} "
                f"(code: {error.get('code', 'unknown')})"
            )
            
        return self.data.get("result")
        
    @property
    def id(self) -> str:
        """
        Get the request ID from the response.
        
        Returns:
            The request ID
        """
        return self.data.get("id")
        
    @property
    def jsonrpc(self) -> str:
        """
        Get the JSON-RPC version from the response.
        
        Returns:
            The JSON-RPC version
        """
        return self.data.get("jsonrpc")
        
    @property
    def testnet(self) -> bool:
        """
        Check if the response is from testnet.
        
        Returns:
            True if the response is from testnet, False otherwise
        """
        return self.data.get("testnet", False)
        
    @property
    def performance_metrics(self) -> Dict[str, int]:
        """
        Get performance metrics from the response.
        
        Returns:
            Dictionary containing performance metrics
        """
        return {
            "usIn": self.data.get("usIn", 0),
            "usOut": self.data.get("usOut", 0),
            "usDiff": self.data.get("usDiff", 0)
        } 