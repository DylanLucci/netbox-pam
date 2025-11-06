from django import forms
from django.utils.translation import gettext_lazy as _
from virtualization.models import VirtualMachine

from dcim.models import Device
from netbox.forms import NetBoxModelFilterSetForm
from tenancy.models import Contact
from utilities.forms.fields import DynamicModelMultipleChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet

from ..models import DeviceGroup, UserGroup

__all__ = (
    'DeviceGroupFilterForm',
    'UserGroupFilterForm',
)


class DeviceGroupFilterForm(NetBoxModelFilterSetForm):
    model = DeviceGroup
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('device_id', 'vm_id', name=_('Attributes')),
    )
    selector_fields = ('filter_id', 'q', 'device_id', 'vm_id')

    name = forms.CharField(
        label=_('Name'),
        required=False
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        label=_('Device'),
        required=False
    )
    vm_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        label=_('Virtual Machine'),
        required=False,
    )
    tag = TagFilterField(model)


class UserGroupFilterForm(NetBoxModelFilterSetForm):
    model = UserGroup
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('contact_id', 'devicegroup_id', name=_('Attributes')),
    )
    selector_fields = ('filter_id', 'q', 'contact_id', 'devicegroup_id')

    name = forms.CharField(
        label=_('Name'),
        required=False
    )
    contact_id = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        label=_('Contact'),
        required=False
    )
    devicegroup_id = DynamicModelMultipleChoiceField(
        queryset=DeviceGroup.objects.all(),
        label=_('Device Group'),
        required=False,
    )
    tag = TagFilterField(model)
