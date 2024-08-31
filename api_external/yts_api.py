from typing import Dict

import requests

from api_external.api_client import ApiClient


class YtsApiClient(ApiClient):
    def get(self, url: str, params: Dict[str, str]) -> dict:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
