from django import forms
from django.utils.translation import gettext_lazy as _
from virtualization.models import VirtualMachine

from dcim.models import Device
from netbox.forms import NetBoxModelBulkEditForm
from tenancy.models import Contact
from utilities.forms.fields import CommentField, DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet

from ..models import DeviceGroup, UserGroup

__all__ = (
    'DeviceGroupBulkEditForm',
    'UserGroupBulkEditForm',
)


class DeviceGroupBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(
        max_length=200,
        required=False,
        label=_('Description')
    )
    devices = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label=_('Devices'),
        selector=True
    )
    vms = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label=_('Virtual Machines'),
        selector=True
    )
    comments = CommentField()

    model = DeviceGroup
    fieldsets = (
        FieldSet('description', name=_('Device Group')),
        FieldSet('devices', 'vms', name=_('Assignment')),
    )
    nullable_fields = ('devices', 'vms', 'description', 'comments')


class UserGroupBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(
        max_length=200,
        required=False,
        label=_('Description')
    )
    contacts = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label=_('Contacts'),
        selector=True
    )
    devicegroups = DynamicModelMultipleChoiceField(
        queryset=DeviceGroup.objects.all(),
        required=False,
        label=_('Device Group'),
        selector=True
    )
    comments = CommentField()

    model = UserGroup
    fieldsets = (
        FieldSet('description', name=_('Device Group')),
        FieldSet('contacts', 'devicegroups', name=_('Assignment')),
    )
    nullable_fields = ('contacts', 'devicegroups', 'description', 'comments')
