import os


class APIConfig:

    API_KEY = os.getenv("weather_api_key")
    API_URL = "https://api.openweathermap.org/data/2.5/forecast"