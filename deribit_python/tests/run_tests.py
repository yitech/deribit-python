"""
Test runner script for the Deribit Python wrapper.
"""
import unittest
import sys
import os

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the test modules
from tests.test_jsonrpc import TestJsonRpcRequest, TestJsonRpcResponse
from tests.test_client import TestDeribitClient
from tests.test_exceptions import TestExceptions
from tests.test_utils import TestUtils


def run_tests():
    """Run all the tests."""
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add the test classes to the suite
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestJsonRpcRequest))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestJsonRpcResponse))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDeribitClient))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestExceptions))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUtils))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return the exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests()) 