import unittest
import os
import json
from unittest.mock import patch
from utils import save_customer_info

class TestSaveCustomerInfo(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.test_filename = "test_customer_info.txt"

    def tearDown(self):
        # Remove the temporary file after testing
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_save_customer_info_success(self):
        data = {"name": "John Doe", "email": "john.doe@example.com"}
        result = save_customer_info(data, self.test_filename)
        self.assertTrue(result)

        # Verify that the data was written to the file
        with open(self.test_filename, "r") as f:
            content = f.readline().strip()
            self.assertEqual(json.loads(content), data)

    def test_save_customer_info_file_error(self):
        # Mock the open function to raise an IOError
        with patch("builtins.open", side_effect=IOError("Mocked IOError")):
            data = {"name": "John Doe", "email": "john.doe@example.com"}
            result = save_customer_info(data, self.test_filename)
            self.assertFalse(result)

    def test_save_customer_info_json_error(self):
        # Mock the json.dumps function to raise a JSONDecodeError
        with patch("json.dumps", side_effect=json.JSONDecodeError("Mocked JSONDecodeError", "doc", 0)):
            data = {"name": "John Doe", "email": "john.doe@example.com"}
            result = save_customer_info(data, self.test_filename)
            self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
