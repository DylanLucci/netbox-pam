from netbox.plugins import PluginMenu, PluginMenuItem

pam_items = (
    PluginMenuItem(
        link='plugins:netbox_pam:jumpcloud_sync',
        link_text='Jumpcloud Sync',
    ),
)

menu = PluginMenu(
    label='PAM',
    groups=(('Sync', pam_items),),
    icon_class='mdi mdi-account-group',
)
