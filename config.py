import os

class Config(object):
    # ...
    FRED_API_KEY = os.environ.get('FRED_API_KEY')

    # Public Endpoints
    OPEN_WEATHER_ONECALL_URL = "https://api.openweathermap.org/data/2.5/onecall"
    FRED_SERIES_URL = "https://api.stlouisfed.org/fred/series"
    FRED_SERIES_DATA_URL = "https://api.stlouisfed.org/fred/series/observations"
