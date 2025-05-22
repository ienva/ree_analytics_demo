import time
import requests
from datetime import datetime, timedelta
import json
import pytz
from config.config import select_token

API_TOKEN = select_token(key='ree_api')
HEADERS = {
    'Accept': 'application/json; application/vnd.esios-api-v1+json',
    'Content-Type': 'application/json',
    'x-api-key': API_TOKEN
}

# The max real-time that can be generated will be hourly
def fetch_data(indicator_id, params):
    url = url = f'https://api.esios.ree.es/indicators/{indicator_id}'

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    print(response.status_code)
    return response.json()

def get_date_values(period):
    datetime_now = datetime.now(pytz.timezone('UTC'))
    datetime_now_start_of_hour = datetime_now.replace(second=0, microsecond=0) - timedelta(seconds=1)
    previous_datetime = datetime_now_start_of_hour - timedelta(minutes=period) + timedelta(seconds=1)
    print(datetime_now_start_of_hour, previous_datetime)
    return datetime_now_start_of_hour, previous_datetime

def get_date_values_future(period):
    datetime_now = datetime.now(pytz.timezone('UTC'))
    datetime_now_start_of_hour = datetime_now.replace(second=0, microsecond=0) + timedelta(minutes=period) - timedelta(seconds=1)
    previous_datetime = datetime_now_start_of_hour - timedelta(minutes=period) + timedelta(seconds=1)
    print(datetime_now_start_of_hour, previous_datetime)
    return datetime_now_start_of_hour, previous_datetime

def get_rt_demand_peninsular():
    datetime_now_start_of_hour, previous_datetime = get_date_values(period=30)
    indicator_id = 1293
    parameters = {
        'start_date': previous_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), 
        'end_date': datetime_now_start_of_hour.strftime("%Y-%m-%dT%H:%M:%SZ")
                  }
    data = fetch_data(indicator_id, parameters)
    format_data = processing_data(data)
    return format_data

def get_rt_demand_nacional():
    indicator_ids = [2037, 2052, 2053, 2054]
    datetime_now_start_of_hour, previous_datetime = get_date_values(period=30)
    parameters = {
        'start_date': previous_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), 
        'end_date': datetime_now_start_of_hour.strftime("%Y-%m-%dT%H:%M:%SZ")
                  }
    # parameters = {}
    data_demand_all = []
    for indicator_id in indicator_ids:
        print(indicator_id)
        data = fetch_data(indicator_id, parameters)
        format_data = processing_data(data)
        data_demand_all = data_demand_all + format_data
    return data_demand_all

def get_generation():
    indicator_ids = [2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047,
                      2048, 2049, 2050, 2051]
    datetime_now_start_of_hour, previous_datetime = get_date_values(period=30)
    parameters = {
        'start_date': previous_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), 
        'end_date': datetime_now_start_of_hour.strftime("%Y-%m-%dT%H:%M:%SZ")
                  }
    data_generation_all = []
    for indicator_id in indicator_ids:
        print(indicator_id)
        data = fetch_data(indicator_id, parameters)
        formatted_data = processing_data(data)
        data_generation_all = data_generation_all + formatted_data
    return data_generation_all

def get_renewable_non_generation():
    indicator_ids = [10351, 10352, 10353, 10354]
    datetime_now_start_of_hour, previous_datetime = get_date_values(period=30)
    parameters = {
        'start_date': previous_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), 
        'end_date': datetime_now_start_of_hour.strftime("%Y-%m-%dT%H:%M:%SZ")
                  }
    data_generation_all = []
    for indicator_id in indicator_ids:
        print(indicator_id)
        data = fetch_data(indicator_id, parameters)
        formatted_data = processing_data(data)
        data_generation_all = data_generation_all + formatted_data
    return data_generation_all

def get_spot_costs():
    datetime_now_start_of_hour, previous_datetime = get_date_values_future(period=1440)
    indicator_id = 600
    parameters = {
        'start_date': previous_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), 
        'end_date': datetime_now_start_of_hour.strftime("%Y-%m-%dT%H:%M:%SZ")
                  }
    data = fetch_data(indicator_id, parameters)
    format_data = processing_data(data)
    return format_data

def get_indicators():
    url = url = f'https://api.esios.ree.es/indicators'
    
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def processing_data(data):
    metric_name = data['indicator']['name']
    metric_id = data['indicator']['id']
    last_update = data['indicator']['values_updated_at']
    values = data['indicator']['values']
    data_values = [{**entry, 'metric_id': metric_id, 'metric_name': metric_name, 'last_update': last_update} for entry in values]
    return data_values

# from src.sender.tinybird_sender import send_to_tinybird
# data_spot_costs = get_spot_costs()
# send_to_tinybird(data_spot_costs, 'landing_ds')