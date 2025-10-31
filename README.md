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
    "netbox_pam": {
        'JC_API_KEY': '', # Paste your Jumpcloud API key between the quotes.
    }
}
```