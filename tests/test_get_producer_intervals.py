import unittest
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_producer_intervals(self):
        response = self.app.get('/api/producers')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("min", data)
        self.assertIn("max", data)
        self.assertIsInstance(data["min"], list)
        self.assertIsInstance(data["max"], list)
        # Check the format of the response data for min and max lists
        self._assert_list_format(data["min"])
        self._assert_list_format(data["max"])


    def _assert_list_format(self, data_list):
        self.assertIsInstance(data_list, list)
        for item in data_list:
            self.assertIsInstance(item, dict)
            self.assertIn("producer", item)
            self.assertIsInstance(item["producer"], str)
            self.assertIn("interval", item)
            self.assertIsInstance(item["interval"], int)
            self.assertIn("previousWin", item)
            self.assertIsInstance(item["previousWin"], int)
            self.assertIn("followingWin", item)
            self.assertIsInstance(item["followingWin"], int)

if __name__ == '__main__':
    unittest.main()
