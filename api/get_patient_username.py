import os 
from dotenv import load_dotenv
import requests
load_dotenv()
URL = os.getenv("URL")
API_KEY = os.getenv("API_KEY")

def get_patient_username(chat_id):
    url = f'{URL}/v1/api/getPatient'
    data = {
        "jsonrpc": "2.0",
        "params": {
            'chat_id': chat_id
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization ': f'Bearer {API_KEY}'
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json().get('result')
        
            return result
        else:
            return f"Failed to get data from Odoo. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request failed: {e}"