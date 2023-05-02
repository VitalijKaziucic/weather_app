import requests
from api_config import APIConfig


class WeatherApi:
    API_KEY = APIConfig.API_KEY
    city_url = APIConfig.API_URL

    def __init__(self, city):
        self.city = city

    def get_api_data(self):
        payload = {"q": self.city,
                   "units": "metric",
                   "appid": self.API_KEY}

        response = requests.get(self.city_url, params=payload)
        return response.json()


