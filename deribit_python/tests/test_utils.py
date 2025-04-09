"""
Tests for the utils module.
"""
import unittest
from unittest.mock import patch

from deribit_python.utils import generate_signature, get_timestamp


class TestUtils(unittest.TestCase):
    """Test the utility functions."""

    def test_generate_signature(self):
        """Test the generate_signature function."""
        api_secret = "test_secret"
        data = {"param1": "value1", "param2": 42}
        
        # Generate the signature
        signature = generate_signature(api_secret, data)
        
        # Check that the signature is a string
        self.assertIsInstance(signature, str)
        
        # Check that the signature is not empty
        self.assertTrue(signature)
        
        # Check that the signature is consistent
        signature2 = generate_signature(api_secret, data)
        self.assertEqual(signature, signature2)
        
        # Check that different data produces different signatures
        data2 = {"param1": "value2", "param2": 42}
        signature3 = generate_signature(api_secret, data2)
        self.assertNotEqual(signature, signature3)
        
        # Check that different secrets produce different signatures
        api_secret2 = "test_secret2"
        signature4 = generate_signature(api_secret2, data)
        self.assertNotEqual(signature, signature4)

    @patch("time.time")
    def test_get_timestamp(self, mock_time):
        """Test the get_timestamp function."""
        # Set up the mock to return a specific time
        mock_time.return_value = 1234567890.123
        
        # Get the timestamp
        timestamp = get_timestamp()
        
        # Check that the timestamp is an integer
        self.assertIsInstance(timestamp, int)
        
        # Check that the timestamp is in milliseconds
        self.assertEqual(timestamp, 1234567890123)
        
        # Check that the mock was called
        mock_time.assert_called_once()


if __name__ == "__main__":
    unittest.main() 