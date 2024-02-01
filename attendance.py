from math import radians, cos, sin, asin, sqrt
from dotenv import load_dotenv
import os
import requests

URL = os.getenv('URL')



def haversine(lon1, lat1, lon2, lat2):
    # Convert latitude and longitude from degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r
# Post attendance to Odoo from post request method
def postAttendance(chat_id):
    url = f'{URL}/api/checkIn'
    data = {
        "jsonrpc": "2.0",
        "params": {
            'chat_id': chat_id,
        }
    }
    headers = {
        'Content-Type': 'application/json'
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

# get address from Odoo from get reqesut method 
def getAddress():
    url = f'{URL}/api/getAddress'
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return f"Failed to get data from Odoo. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request failed: {e}"

def isStaff(chat_id):
    url = f'{URL}/api/isStaff'
    data = {
        "jsonrpc": "2.0",
        "params": {
            'chat_id': chat_id
        }
    }
    headers = {
        'Content-Type': 'application/json'
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