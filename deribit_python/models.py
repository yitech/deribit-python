from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import uuid
import json


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