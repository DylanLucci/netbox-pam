from netbox.plugins import PluginTemplateExtension


class SyncJumpcloudUsersButton(PluginTemplateExtension):
    model = 'tenancy.contact'

    def list_buttons(self):
        return self.render('netbox_pam/inc/jumpcloud_sync_button.html')

template_extensions = [
    SyncJumpcloudUsersButton,
]
