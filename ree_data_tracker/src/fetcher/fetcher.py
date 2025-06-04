import requests
from datetime import datetime, timedelta
import pytz
import time
from config.config import select_token
from config.logging_config import setup_logger

logger = setup_logger('fetcher')

def get_headers():
    API_TOKEN = select_token(key='ree_api')
    return {
        'Accept': 'application/json; application/vnd.esios-api-v1+json',
        'Content-Type': 'application/json',
        'x-api-key': API_TOKEN
    }

# The max real-time that can be generated will be hourly
def fetch_data(indicator_id, params, retries=3, delay=2):
    url = f'https://api.esios.ree.es/indicators/{indicator_id}'
    headers = get_headers()
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Attempt {attempt+1} failed for indicator {indicator_id}: {str(e)}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                logger.error(f"All {retries} attempts failed for indicator {indicator_id}")
                return None

def get_date_values(period):
    datetime_now = datetime.now(pytz.timezone('UTC'))
    datetime_now_start_of_hour = datetime_now.replace(second=0, microsecond=0) - timedelta(seconds=1)
    previous_datetime = datetime_now_start_of_hour - timedelta(minutes=period) + timedelta(seconds=1)
    logger.debug(f"Date range: {datetime_now_start_of_hour} to {previous_datetime}")
    return datetime_now_start_of_hour, previous_datetime

def get_date_values_future(period):
    datetime_now = datetime.now(pytz.timezone('UTC'))
    datetime_now_start_of_hour = datetime_now.replace(second=0, microsecond=0) + timedelta(minutes=period) - timedelta(seconds=1)
    previous_datetime = datetime_now_start_of_hour - timedelta(minutes=period) + timedelta(seconds=1)
    logger.debug(f"Future date range: {datetime_now_start_of_hour} to {previous_datetime}")
    return datetime_now_start_of_hour, previous_datetime

def get_rt_demand_peninsular():
    logger.info("Fetching peninsular demand data")
    datetime_now_start_of_hour, previous_datetime = get_date_values(period=60)
    indicator_id = 1293
    parameters = {
        'start_date': previous_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), 
        'end_date': datetime_now_start_of_hour.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    data = fetch_data(indicator_id, parameters)
    format_data = processing_data(data)
    logger.info(f"Retrieved {len(format_data)} peninsular demand records")
    return format_data

def get_rt_demand_nacional():
    logger.info("Fetching national demand data")
    indicator_ids = [2037, 2052, 2053, 2054]
    datetime_now_start_of_hour, previous_datetime = get_date_values(period=60)
    parameters = {
        'start_date': previous_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), 
        'end_date': datetime_now_start_of_hour.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    data_demand_all = []
    for indicator_id in indicator_ids:
        logger.debug(f"Fetching national demand indicator {indicator_id}")
        data = fetch_data(indicator_id, parameters)
        format_data = processing_data(data)
        data_demand_all = data_demand_all + format_data
    logger.info(f"Retrieved {len(data_demand_all)} national demand records")
    return data_demand_all

def get_generation():
    logger.info("Fetching generation data")
    indicator_ids = [2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047,
                    2048, 2049, 2050, 2051]
    datetime_now_start_of_hour, previous_datetime = get_date_values(period=60)
    parameters = {
        'start_date': previous_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), 
        'end_date': datetime_now_start_of_hour.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    data_generation_all = []
    for indicator_id in indicator_ids:
        logger.debug(f"Fetching generation indicator {indicator_id}")
        data = fetch_data(indicator_id, parameters)
        formatted_data = processing_data(data)
        data_generation_all = data_generation_all + formatted_data
    logger.info(f"Retrieved {len(data_generation_all)} generation records")
    return data_generation_all

def get_renewable_non_generation():
    logger.info("Fetching renewable non-generation data")
    indicator_ids = [10351, 10352, 10353, 10354]
    datetime_now_start_of_hour, previous_datetime = get_date_values(period=60)
    parameters = {
        'start_date': previous_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), 
        'end_date': datetime_now_start_of_hour.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    data_generation_all = []
    for indicator_id in indicator_ids:
        logger.debug(f"Fetching renewable non-generation indicator {indicator_id}")
        data = fetch_data(indicator_id, parameters)
        formatted_data = processing_data(data)
        data_generation_all = data_generation_all + formatted_data
    logger.info(f"Retrieved {len(data_generation_all)} renewable non-generation records")
    return data_generation_all

def get_spot_costs():
    logger.info("Fetching spot costs data")
    datetime_now_start_of_hour, previous_datetime = get_date_values_future(period=1440)
    indicator_id = 600
    parameters = {
        'start_date': previous_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), 
        'end_date': datetime_now_start_of_hour.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    data = fetch_data(indicator_id, parameters)
    format_data = processing_data(data)
    logger.info(f"Retrieved {len(format_data)} spot cost records")
    return format_data

def get_estimated_generation():
    logger.info("Fetching estimated generation data")
    indicator_ids = [542, 543, 10034]
    datetime_now_start_of_hour, previous_datetime = get_date_values(period=60)
    parameters = {
        'start_date': previous_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), 
        'end_date': datetime_now_start_of_hour.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    data_generation_all = []
    for indicator_id in indicator_ids:
        logger.debug(f"Fetching estimated generation indicator {indicator_id}")
        data = fetch_data(indicator_id, parameters)
        formatted_data = processing_data(data)
        data_generation_all = data_generation_all + formatted_data
    logger.info(f"Retrieved {len(data_generation_all)} estimated generation records")
    return data_generation_all

def get_indicators():
    logger.info("Fetching available indicators")
    url = f'https://api.esios.ree.es/indicators'
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def processing_data(data):
    metric_name = data['indicator']['name']
    metric_id = data['indicator']['id']
    last_update = data['indicator']['values_updated_at']
    values = data['indicator']['values']
    data_values = [{**entry, 'metric_id': metric_id, 'metric_name': metric_name, 'last_update': last_update} for entry in values]
    return data_values
