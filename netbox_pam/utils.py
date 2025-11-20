import requests
from django.conf import settings

from netbox.plugins import get_plugin_config

JC_API_KEY = settings.PLUGINS_CONFIG['netbox_pam'].get('JC_API_KEY')
HEADERS = {'x-api-key': JC_API_KEY}


def get_plugin_setting(setting_name):
    return get_plugin_config('netbox_pam', setting_name)


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


def fetch_jumpcloud_resource_single(endpoint):
    """
    Generic single-resource fetcher that returns the JSON payload as-is.

    Args:
        endpoint (str): API endpoint after `/api`, e.g. "systemusers" or "v2/usergroups"

    Returns:
        JSON: The fetched object's JSON
    """
    url = f'https://console.jumpcloud.com/api/{endpoint}'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def fetch_jumpcloud_users(limit=0):
    return fetch_jumpcloud_resource('systemusers', limit)


def fetch_jumpcloud_user(user_id):
    user = fetch_jumpcloud_resource_single(f'systemusers/{user_id}')
    print(user)
    return user


def fetch_jumpcloud_usergroups(limit=0):
    return fetch_jumpcloud_resource('v2/usergroups', limit)


def fetch_jumpcloud_devices(limit=0):
    return fetch_jumpcloud_resource('systems', limit)


def fetch_jumpcloud_devicegroups(limit=0):
    return fetch_jumpcloud_resource('v2/systemgroups', limit)


def fetch_jumpcloud_usergroup_devicegroups(group_id, limit=0):
    return fetch_jumpcloud_resource(f'v2/usergroups/{group_id}/systemgroups', limit)


def fetch_jumpcloud_usergroup_memberships(group_id, limit=0):
    return fetch_jumpcloud_resource(f'v2/usergroups/{group_id}/members', limit)


def fetch_jumpcloud_devicegroup_memberships(group_id, limit=0):
    return fetch_jumpcloud_resource(f'v2/systemgroups/{group_id}/members', limit)


def sync_object(model, lookup, field_map, custom_fields, name_field='name', link_func=None):
    """
    Generic object sync helper.

    Args:
        model: Django model class (e.g. Contact, DeviceGroup)
        lookup: dict for get_or_create lookup (e.g. {'name': name})
        field_map: dict of model fields to update (e.g. {'comments': 'desc'})
        custom_fields: dict of custom field key/value pairs (e.g. {'pam_jc_id': id})
        name_field: field to show in messages (defaults to 'name')
        link_func: optional function returning URL for message links (defaults to obj.get_absolute_url)

    Returns:
        dict: {'message': str, 'created': int, 'updated': int}
    """
    obj, created = model.objects.get_or_create(**lookup, defaults=field_map)
    changed = False

    if created or get_plugin_setting('overwrite_existing_objects'):
        for field, new_value in field_map.items():
            if getattr(obj, field) != new_value:
                setattr(obj, field, new_value)
                changed = True

        cf_data = obj.custom_field_data or {}
        for key, new_value in custom_fields.items():
            if cf_data.get(key) != new_value:
                cf_data[key] = new_value
                changed = True

        if changed:
            obj.custom_field_data = cf_data
            obj.save()

    display_name = getattr(obj, name_field, str(obj))
    url = link_func(obj) if link_func else obj.get_absolute_url()
    action = 'Created' if created else ('Updated' if changed else 'No changes for')

    return {
        'instance': obj,
        'message': f'{action} {model._meta.verbose_name.lower()}: <a href=\"{url}\">{display_name}</a>',
        'created': 1 if created else 0,
        'updated': 1 if changed and not created else 0
    }
