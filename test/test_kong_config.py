import unittest
import requests
import os

KONG_ADMIN_URL = "http://localhost"
KONG_ADMIN_KEY = os.getenv("KONG_ADMIN_KEY", "admin-key")


class TesApiHealth(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method"""

    def test_succesful_auth_call(self):
        """Verify can add kong path"""

        headers = {
            "Content-Type": "application/json",
            "apikey": KONG_ADMIN_KEY
        }

        # 1. Create the FastAPI service
        service_data = {
            "name": "fastapi-backend",
            "url": "http://fastapi-service:8080"
        }

        response = requests.post(
            f"{KONG_ADMIN_URL}/admin/services",
            json=service_data,
            headers=headers
        )
        print(f"Service creation: {response.status_code}")
        print(response.json())

        # 2. Create a route for the service
        route_data = {
            "name": "fastapi-route",
            "paths": ["/"],
            "strip_path": True,
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
        }

        response = requests.post(
            f"{KONG_ADMIN_URL}/admin/services/fastapi-backend/routes",
            json=route_data,
            headers=headers
        )
        print(f"\nRoute creation: {response.status_code}")
        print(response.json())

    def test_no_login_call(self):
        """Test successful user signup"""

        service_data = {
            "name": "fastapi-backend",
            "url": "http://fastapi-service:8080"
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(
            f"{KONG_ADMIN_URL}/admin/services",
            json=service_data,
            headers=headers
        )

        print(response.content)

    def test_api_call(self):
        health = requests.get("http://localhost/items")
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
