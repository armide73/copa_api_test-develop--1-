"""SPENN API Module"""
import requests
from copa.apps.spenn.models import SpennSession
from copa.services.spenn.urls import URLs
from copa.settings import (
    SPENN_API_KEY,
    SPENN_AUTH_API_URL,
    SPENN_CLIENT_ID,
    SPENN_CLIENT_SECRET,
    SPENN_PARTNER_API_URL,
)


class SpennAPI:
    """SPENN API class"""

    def __init__(self, **kwargs):
        self.url = URLs()
        self.api_key = SPENN_API_KEY
        self.client_id = SPENN_CLIENT_ID
        self.client_secret = SPENN_CLIENT_SECRET
        self.auth_api_url = SPENN_AUTH_API_URL
        self.partner_api_url = SPENN_PARTNER_API_URL
        self.headers = {}
        self.headers["Authorization"] = f"Bearer {self.authenticate()}"

    def get(self, url):
        """Get data from KuDiBooks API endpoint"""

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post(self, url, data):
        """Post data to KuDiBooks API endpoint"""
        sess = requests.Session()

        response = sess.post(url, headers=self.headers, json=data)
        response.raise_for_status()

        return response.json()

    def delete(self, url):
        """Delete data from KuDiBooks API endpoint"""
        response = requests.Response()

        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()

        return response.json()

    def put(self, url, data):
        """Put data to KuDiBooks API endpoint"""
        response = requests.Response()

        response = requests.put(url, headers=self.headers, data=data)
        response.raise_for_status()

        return response.json()

    def authenticate(self):
        """Create access token"""
        data = {
            "grant_type": "api_key",
            "api_key": self.api_key,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": "SpennBusiness",
        }

        session = SpennSession.objects.first()

        if session:
            if session.is_token_expired:
                session.delete()
            else:
                return session.access_token

        response = requests.post(
            self.auth_api_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,
        )

        response_data = response.json()

        session = SpennSession.objects.create(
            access_token=response_data.get("access_token"),
            refresh_token=response_data.get("refresh_token"),
            expires_in=response_data.get("expires_in"),
        )

        return session.access_token
