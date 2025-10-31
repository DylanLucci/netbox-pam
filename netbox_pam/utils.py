import json

import requests
from django.conf import settings

JC_API_KEY = settings.PLUGINS_CONFIG['netbox_pam'].get('JC_API_KEY')
HEADERS = {'x-api-key': JC_API_KEY}

def fetch_jumpcloud_resource(endpoint, limit=0, skip=0):
    """
    Helper method for fetching paginated Jumpcloud API resources.

    Args:
        endpoint (str): API endpoint after `/api`, e.g. "systemusers" or "v2/usergroups"
        limit (int): Number of records per request
        skip (int): Number of records to skip (for pagination)
    
    Returns:
        list: A list of resource dictionaries
    """
    url = f'https://console.jumpcloud.com/api/{endpoint}'
    params = {'limit': str(limit), 'skip': str(skip)}

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, dict) and 'results' in data:
        return data['results']
    elif isinstance(data, list):
        return data
    else:
        print(f"Unexpected response format for {endpoint}: {data}")
        return []

def fetch_jumpcloud_users(limit=0):
    return fetch_jumpcloud_resource('systemusers', limit)

def fetch_jumpcloud_usergroups(limit=0):
    return fetch_jumpcloud_resource('v2/usergroups', limit)

def fetch_jumpcloud_devices(limit=0):
    return fetch_jumpcloud_resource('systems', limit)

def fetch_jumpcloud_devicegroups(limit=0):
    return fetch_jumpcloud_resource('v2/systemgroups', limit)

def fetch_jumpcloud_user_memberships(user_id, limit=0):
    return fetch_jumpcloud_resource(f'v2/users/{user_id}/memberof', limit)