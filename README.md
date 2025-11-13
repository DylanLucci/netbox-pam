# NetBox PAM Plugin

A [NetBox](https://github.com/netbox-community/netbox) plugin for Privileged Access Management.

## Features

- Sync users and groups from Jumpcloud to NetBox

## Compatibility

Each plugin version listed has been tested with its corresponding NetBox version.

| Plugin Version | NetBox Version |
|:--------------:|:--------------:|
|     1.0.0      |     4.3.x      |

## Installing

Download the .tar.gz file attached to any release

Add the file path to `local_requirements.txt`:
```txt
netbox-pam @ file:///opt/netbox/plugins/netbox_pam-x.x.x.tar.gz
```

Run `upgrade.sh` on your NetBox install

## Configuration

Enable the plugin in `/opt/netbox/netbox/configuration.py` and add your Jumpcloud API key to the PLUGIN_CONFIG:
```python
PLUGINS = [
    "netbox_pam"
]

PLUGINS_CONFIG = {
    'netbox_pam': {
        'JC_API_KEY': '', # Paste your Jumpcloud API key between the quotes.
    }
}
```

### Settings

If you want to override the defaults for the plugin, you can do so in `/opt/netbox/netbox/netbox/configuration.py`, or if you use netbox-docker, your `/configuration/plugins.py` file :

```python
PLUGINS = [
    'netbox_pam'
]

PLUGINS_CONFIG = {
    'netbox_pam': {
        'JC_API_KEY': '',
        # Example settings below, see "Available settings"
        # in README.md for all possible settings
        'overwrite_existing_objects': False,
    }
}
```

#### Available Settings
| Setting | Default value | Description |
|---------|---------------|-------------|
| `overwrite_existing_objects` | `False`| When syncing an object from Jumpcloud, fields on existing NetBox objects will be overwritten. |
