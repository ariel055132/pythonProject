import time
from typing import Dict, List
import requests

def request_get(base_url, params):
    r = requests.get(base_url, params=params)
    if r.status_code != requests.codes.ok:
        print(f'Error: {r.status_code}')
    try:
        data = r.json()
        if data['status'] != 200:
            print(f"Error: {data['msg']}")
            return None
    except Exception as e:
        print(e)
        return None
    return data['data']