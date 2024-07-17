import os
from dotenv import load_dotenv
import requests

load_dotenv()
URL = os.getenv("URL")
API_KEY = os.getenv("API_KEY")

def get_patient_username(chat_id):
    url = f'{URL}/v1/api/getPatient?chat_id={chat_id}'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json().get('result')
            return result
        else:
            print(f"Failed to get data from Odoo. Status code: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []