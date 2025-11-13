
import django_tables2 as tables
from django.utils.translation import gettext as _
from netbox.tables import NetBoxTable, columns

from .models import DeviceGroup, UserGroup

__all__ = (
    'DeviceGroupTable',
    'UserGroupTable',
)


class DeviceGroupTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    devices = columns.ManyToManyColumn(
        linkify_item=True,
        verbose_name=_('Devices')
    )
    vms = columns.ManyToManyColumn(
        linkify_item=True,
        verbose_name=_('Virtual Machines')
    )
    tags = columns.TagColumn(
        url_name='plugins:netbox_pam:devicegroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = DeviceGroup
        fields = (
            'pk', 'id', 'name', 'description', 'devices', 'vms', 'comments', 'tags', 'actions', 'created',
            'last_updated',
        )
        default_columns = ('pk', 'name', 'devices', 'vms', 'tags')


class UserGroupTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    contacts = columns.ManyToManyColumn(
        linkify_item=True,
        verbose_name=_('Contacts')
    )
    devicegroups = columns.ManyToManyColumn(
        linkify_item=True,
        verbose_name=_('Device Groups')
    )
    tags = columns.TagColumn(
        url_name='plugins:netbox_pam:usergroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = UserGroup
        fields = (
            'pk', 'id', 'name', 'description', 'contacts', 'devicegroups', 'comments', 'tags', 'actions', 'created',
            'last_updated',
        )
        default_columns = ('pk', 'name', 'contacts', 'devicegroups', 'tags')
