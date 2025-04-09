"""
Tests for the exceptions module.
"""
import unittest

from deribit_python.exceptions import (
    DeribitAPIError,
    DeribitAuthenticationError,
    DeribitRequestError,
    DeribitResponseError
)


class TestExceptions(unittest.TestCase):
    """Test the exception classes."""

    def test_deribit_api_error(self):
        """Test the DeribitAPIError class."""
        error = DeribitAPIError("Test error message")
        self.assertEqual(str(error), "Test error message")
        self.assertIsInstance(error, Exception)

    def test_deribit_authentication_error(self):
        """Test the DeribitAuthenticationError class."""
        error = DeribitAuthenticationError("Authentication failed")
        self.assertEqual(str(error), "Authentication failed")
        self.assertIsInstance(error, DeribitAPIError)
        self.assertIsInstance(error, Exception)

    def test_deribit_request_error(self):
        """Test the DeribitRequestError class."""
        error = DeribitRequestError("Request failed")
        self.assertEqual(str(error), "Request failed")
        self.assertIsInstance(error, DeribitAPIError)
        self.assertIsInstance(error, Exception)

    def test_deribit_response_error(self):
        """Test the DeribitResponseError class."""
        error = DeribitResponseError("Response parsing failed")
        self.assertEqual(str(error), "Response parsing failed")
        self.assertIsInstance(error, DeribitAPIError)
        self.assertIsInstance(error, Exception)


if __name__ == "__main__":
    unittest.main() 