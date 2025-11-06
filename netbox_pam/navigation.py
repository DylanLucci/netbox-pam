from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

groups_items = (
    PluginMenuItem(
        link='plugins:netbox_pam:devicegroup_list',
        link_text='Device Groups',
        permissions=['netbox_pam.view_devicegroup'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_pam:devicegroup_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=['netbox_pam.add_devicegroup'],
            ),
            PluginMenuButton(
                link='plugins:netbox_pam:devicegroup_bulk_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=['netbox_pam.add_devicegroup'],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_pam:usergroup_list',
        link_text='User Groups',
        permissions=['netbox_pam.view_usergroup'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_pam:usergroup_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=['netbox_pam.add_usergroup'],
            ),
            PluginMenuButton(
                link='plugins:netbox_pam:usergroup_bulk_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=['netbox_pam.add_usergroup'],
            ),
        ),
    ),
)

sync_items = (
    PluginMenuItem(
        link='plugins:netbox_pam:jumpcloud_sync',
        link_text='Jumpcloud Sync',
    ),
)

menu = PluginMenu(
    label='PAM',
    groups=(
        ('Groups', groups_items),
        ('Sync', sync_items),
    ),
    icon_class='mdi mdi-account-group',
)
