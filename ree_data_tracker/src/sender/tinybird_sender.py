import json
import requests
from config.config import select_token
import time
from config.logging_config import setup_logger

logger = setup_logger('tinybird_sender')

def get_headers():
    TOKEN = select_token(key='tinybird')
    return {'Authorization': f'Bearer {TOKEN}'}

def send_to_tinybird(payload, datasource, retries=3, delay=2):
    if not payload:
        logger.warning(f"No data to send to Tinybird datasource {datasource}")
        return True
        
    headers = get_headers()
    for attempt in range(retries):
        try:
            response = requests.post(
                f'https://api.tinybird.co/v0/events?name={datasource}',
                headers=headers,
                data="\n".join(json.dumps(record) for record in payload)
            )
            response.raise_for_status()
            response_data = response.json()
            logger.info(f"Successfully sent {len(payload)} records to Tinybird {datasource}: {response_data}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Attempt {attempt+1} to send to Tinybird failed: {str(e)}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                logger.error(f"All {retries} attempts to send to Tinybird failed")
                return False
