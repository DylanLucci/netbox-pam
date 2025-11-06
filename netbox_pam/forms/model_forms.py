from django.utils.translation import gettext_lazy as _
from virtualization.models import VirtualMachine

from dcim.models import Device
from netbox.forms import NetBoxModelForm
from tenancy.models import Contact
from utilities.forms.fields import CommentField, DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet

from ..models import DeviceGroup, UserGroup

__all__ = (
    'DeviceGroupForm',
    'UserGroupForm',
)


class DeviceGroupForm(NetBoxModelForm):
    devices = DynamicModelMultipleChoiceField(
        queryset = Device.objects.all(),
        selector=True,
        label=_('Devices'),
        required=False
    )
    vms = DynamicModelMultipleChoiceField(
        queryset = VirtualMachine.objects.all(),
        selector=True,
        label=_('Virtual Machines'),
        required=False
    )
    comments = CommentField()

    fieldsets = (
        FieldSet('name', 'description', 'tags', name=_('Device Group')),
        FieldSet('devices', 'vms', name=_('Assignments')),
    )

    class Meta:
        model = DeviceGroup
        fields = ('name', 'description', 'devices', 'vms', 'comments', 'tags')


class UserGroupForm(NetBoxModelForm):
    contacts = DynamicModelMultipleChoiceField(
        queryset = Contact.objects.all(),
        selector=True,
        label=_('Contacts'),
        required=False
    )
    devicegroups = DynamicModelMultipleChoiceField(
        queryset = DeviceGroup.objects.all(),
        selector=True,
        label=_('Device Groups'),
        required=False
    )
    comments = CommentField()

    fieldsets = (
        FieldSet('name', 'description', 'tags', name=_('User Group')),
        FieldSet('contacts', 'devicegroups', name=_('Assignments')),
    )

    class Meta:
        model = UserGroup
        fields = ('name', 'description', 'contacts', 'devicegroups', 'comments', 'tags')
