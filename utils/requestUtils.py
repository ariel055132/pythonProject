import time
from typing import Dict, List, Any, Optional
import requests

def request_get(base_url: str, params: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    r = requests.get(base_url, params=params, timeout=30)
    if r.status_code != requests.codes.ok:
        print(f'Error: {r.status_code}')
    try:
        data = r.json()
        if data['status'] != 200:
            print(f"Error: {data['msg']}")
            return None
    except (ValueError, KeyError, TypeError) as e:
        logger.error(f"JSON parsing error: {e}") 
        return None
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
    return data['data']