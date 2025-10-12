import unittest
import requests
import os

KONG_ADMIN_URL = "http://localhost"
KONG_ADMIN_KEY = os.getenv("KONG_ADMIN_KEY", "admin-key")


class TesApiHealth(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method"""

    def test_add_n8n_route(self):
        """Verify can add kong path with hostname-based route"""

        headers = {
            "Content-Type": "application/json",
            "apikey": KONG_ADMIN_KEY
        }

        # 1. Create the FastAPI service
        service_data = {
            "name": "n8n",
            "url": "http://n8n:5678"
        }

        response = requests.post(
            f"{KONG_ADMIN_URL}/admin/services",
            json=service_data,
            headers=headers
        )
        print(f"Service creation: {response.status_code}")
        print(response.json())

        # 2. Create a route for the service based on the Host header
        route_data = {
            "name": "n8n-route",
            "hosts": ["n8n.user.localhost"],  # 👈 match based on host
            "strip_path": True,
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
        }

        response = requests.post(
            f"{KONG_ADMIN_URL}/admin/services/n8n/routes",
            json=route_data,
            headers=headers
        )
        print(f"\nRoute creation: {response.status_code}")
        print(response.json())

    def test_api_call(self):
        health = requests.get("http://n8n.user.localhost/signin")
        print(health.content)
        self.assertIn(health.status_code, [200, 201])

    def tearDown(self):
        """Clean up after each test"""
        # Add any cleanup code here if needed
        # For example, delete test users from database
        pass


if __name__ == '__main__':
    # Run with more verbose output
    unittest.main(verbosity=2)

    # Alternative: Run specific test
    # unittest.main(defaultTest='TestSignupAPI.test_successful_signup')
