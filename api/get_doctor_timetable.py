import os 
from dotenv import load_dotenv
import requests
import datetime

load_dotenv()
URL = os.getenv("URL")
API_KEY = os.getenv("API_KEY")

def get_doctor_timetable():
    # Get current month 
    now = datetime.datetime.now()
    current_month = now.strftime("%B")
    
    # Construct the URL with query parameters
    url = f'{URL}/v1/api/doctor_timetable?month={current_month}'
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