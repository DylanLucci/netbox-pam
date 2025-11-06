from django.utils.translation import gettext_lazy as _
from virtualization.models import VirtualMachine

from dcim.models import Device
from netbox.forms import NetBoxModelImportForm
from tenancy.models import Contact
from utilities.forms.fields import CSVModelMultipleChoiceField

from ..models import DeviceGroup, UserGroup

__all__ = (
    'DeviceGroupImportForm',
    'UserGroupImportForm',
)


class DeviceGroupImportForm(NetBoxModelImportForm):
    devices = CSVModelMultipleChoiceField(
        queryset=Device.objects.all(),
        label=_('Devices'),
        required=False,
        to_field_name='name',
        help_text=_('Devices that belong to this device group')
    )
    vms = CSVModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        label=_('Virtual Machines'),
        required=False,
        to_field_name='name',
        help_text=_('Virtual machines that belong to this device group')
    )

    class Meta:
        model = DeviceGroup
        fields = ('name', 'description', 'devices', 'vms', 'comments', 'tags')


class UserGroupImportForm(NetBoxModelImportForm):
    contacts = CSVModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        label=_('Contacts'),
        required=False,
        to_field_name='name',
        help_text=_('Contacts that belong to this user group')
    )
    devicegroups = CSVModelMultipleChoiceField(
        queryset=DeviceGroup.objects.all(),
        label=_('Device Groups'),
        required=False,
        to_field_name='name',
        help_text=_('Device groups that belong to this user group')
    )

    class Meta:
        model = UserGroup
        fields = ('name', 'description', 'contacts', 'devicegroups', 'comments', 'tags')
