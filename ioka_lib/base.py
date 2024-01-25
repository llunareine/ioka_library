import requests
import os
from dotenv import load_dotenv

load_dotenv()


class ConvertToObj:
    def init(self, **entries):
        self.dict.update(entries)

    def repr(self):
        attributes = ', '.join(f"{key}={value!r}" for key, value in self.dict.items())
        return f"{attributes}"
    def str(self):
        attributes = ', '.join(f"{key}: {value}" for key, value in self.dict.items())
        return f"{attributes}"

class Response:
    def init(self, data):
        if isinstance(data, list):
            self.data = [ConvertToObj(**item) for item in data]
        else:
            self.data = ConvertToObj(**data)


class BaseAPI:

    def init(self, api_key):
        self.base_url = "https://stage-api.ioka.kz/v2"
        self.api_key = api_key

    def _send_request(self, method, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.request(method, url, headers=headers, json=data)
        if method == 'DELETE' and response.status_code == 204:
            return 'Successfully deleted'
        if 400 <= response.status_code < 600:
            return response.json()['message']

        if isinstance(response.json(), list):
            return Response(response.json())
        else:
            return ConvertToObj(**response.json())