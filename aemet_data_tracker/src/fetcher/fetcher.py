import requests
from ree_data_tracker.src.config.config import select_token


def get_headers():
    API_TOKEN = select_token(key='ree_api')
    return {
        'api_key': API_TOKEN
    }

def get_weather_stations():
    url = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/'
    headers = {
    'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

get_weather_stations()