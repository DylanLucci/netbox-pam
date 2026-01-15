from netbox.plugins import PluginConfig

from .version import __version__


class NetBoxJumpcloudSyncConfig(PluginConfig):
    name = 'netbox_pam'
    verbose_name = 'NetBox PAM'
    version = __version__
    description = 'Privileged Access Management in NetBox'
    author = 'Dylan Lucci'
    author_email = 'dylan@sol1.com.au'
    base_url = 'pam'
    min_version = '4.3.0'
    default_settings = {
        'overwrite_existing_objects': False,
    }

config = NetBoxJumpcloudSyncConfig
