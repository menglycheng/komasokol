from math import radians, sin, cos, sqrt, asin
from dotenv import load_dotenv
import os
import requests

URL = os.getenv('URL')



def haversine(user_lat, user_long, center_lat, center_long, radius):
    # Convert latitude and longitude from degrees to radians
    user_lat, user_long, center_lat, center_long = map(radians, [user_lat, user_long, center_lat, center_long])
    # Haversine formula
    dlon = center_long - user_long
    dlat = center_lat - user_lat
    a = sin(dlat / 2) ** 2 + cos(user_lat) * cos(center_lat) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r_earth = 6371000  # Earth's radius in meters

    # Calculate distance and check if it's within the specified radius
    distance = c * r_earth
    return distance <= radius

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