
import os 
from dotenv import load_dotenv
import requests
load_dotenv()
URL = os.getenv("URL")
API_KEY = os.getenv("API_KEY")


def checkPremium():
    url = f'{URL}/v1/api/is-premium'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'

    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Request failed with status code {response.status_code}"
   
    except requests.RequestException as e:
        return f"Request failed : {e}"