"""Kudibooks API
"""
from django.http import HttpResponse
import requests

from copa.services.kudibooks.urls import URLs
from copa.settings import KUDIBOOKS_API_KEY


class KudiBooksAPI:
    """KudiBooks API class"""

    def __init__(self, **kwargs):
        self.api_key = KUDIBOOKS_API_KEY
        self.url = URLs()

        user_code = kwargs.get('user_code')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'User-Code': user_code,
            'Accept': 'application/json',
        }

    def get(self, url):
        """Get data from KuDiBooks API endpoint"""
        response = HttpResponse()
        response = requests.get(
            url,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def post(self, url, data):
        """Post data to KuDiBooks API endpoint"""
        response = requests.Response()
            
        response = requests.post(
            url,
            headers=self.headers,
            data=data
        )
        response.raise_for_status()

        return response.json()

    def delete(self, url):
        """Delete data from KuDiBooks API endpoint"""
        response = requests.Response()

        response = requests.delete(
            url,
            headers=self.headers
        )
        response.raise_for_status()

        return response.json()

    def put(self, url, data):
        """Put data to KuDiBooks API endpoint"""
        response = requests.Response()

        response = requests.put(
            url,
            headers=self.headers,
            data=data
        )
        response.raise_for_status()

        return response.json()
