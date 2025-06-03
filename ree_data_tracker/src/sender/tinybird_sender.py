import json
import requests
from config.config import select_token
import time

def get_headers():
    TOKEN = select_token(key='tinybird')
    return {'Authorization': f'Bearer {TOKEN}'}

def send_to_tinybird(payload, datasource, retries=3, delay=2):
    headers = get_headers()
    for attempt in range(retries):
        try:
            response = requests.post(
                f'https://api.tinybird.co/v0/events?name={datasource}',
                headers=headers,
                data="\n".join(json.dumps(record) for record in payload)
            )
            response.raise_for_status()
            print(response.json())
            return True
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} to send to Tinybird failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print(f"All {retries} attempts to send to Tinybird failed.")
                return False
