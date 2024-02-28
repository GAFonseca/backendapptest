import unittest
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_invalid_endpoint(self):
        response = self.app.get('/api/nonexistent-endpoint')
        self.assertEqual(response.status_code, 404)
        error_data = response.json
        self.assertIn("error", error_data)
        self.assertEqual(error_data["error"], "Endpoint not found")

if __name__ == '__main__':
    unittest.main()