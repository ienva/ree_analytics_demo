import json
import requests
from config.config import select_token

TOKEN = select_token(key='tinybird')
HEADERS = {
            'Authorization': f'Bearer {TOKEN}',
        }

def send_to_tinybird(payload, datasource):
    response = requests.post(
        f'https://api.tinybird.co/v0/events?name={datasource}',
        headers=HEADERS,
        data="\n".join(json.dumps(record) for record in payload)
    )
    response.raise_for_status()
    print(response.json())
