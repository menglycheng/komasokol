import os 
from dotenv import load_dotenv
import requests
load_dotenv()
URL = os.getenv("URL")
API_KEY = os.getenv("API_KEY")

def check_user_connect(chat_id):
    url = f'{URL}/v1/api/checkUser?chat_id={chat_id}'
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
            return f"Failed to get data from Odoo. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request failed: {e}"