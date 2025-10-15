import unittest
import requests
import os

KONG_ADMIN_URL = "https://ognastack.com"
KONG_ADMIN_KEY = os.getenv("KONG_ADMIN_KEY", "admin-key")

APP_NAME = 'n8n'
PORT_VALUE = 80
SERVER_HOST = 'ognastack.com'


class TesApiHealth(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method"""

    def test_delete(self):
        """Verify can delete kong route and service"""

        headers = {
            "Content-Type": "application/json",
            "apikey": KONG_ADMIN_KEY
        }

        # 1. Delete the route first (routes must be deleted before the service)
        response = requests.delete(
            f"{KONG_ADMIN_URL}/admin/routes/{APP_NAME}",
            headers=headers
        )
        print(f"Route deletion: {response.status_code}")
        if response.status_code == 204:
            print("Route deleted successfully")
        else:
            print(response.json())

        # 2. Delete the service
        response = requests.delete(
            f"{KONG_ADMIN_URL}/admin/services/{APP_NAME}",
            headers=headers
        )
        print(f"\nService deletion: {response.status_code}")
        if response.status_code == 204:
            print("Service deleted successfully")
        else:
            print(response.json())


    def test_add(self):
        """Verify can add kong path with hostname-based route"""

        headers = {
            "Content-Type": "application/json",
            "apikey": KONG_ADMIN_KEY
        }

        # 1. Create the FastAPI service
        service_data = {
            "name": APP_NAME,
            "url": f"http://{APP_NAME}:{PORT_VALUE}"
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
            "name": f"{APP_NAME}-route",
            "hosts": [f"{APP_NAME}.user.{SERVER_HOST}"],  # 👈 match based on host
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
        health = requests.get(f"http://{APP_NAME}.user.{SERVER_HOST}/signin")
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
