import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _
from virtualization.models import VirtualMachine

from dcim.models import Device
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.models import Contact

from .models import DeviceGroup, UserGroup

__all__ = (
    'DeviceGroupFilterSet',
    'UserGroupFilterSet',
)


class DeviceGroupFilterSet(NetBoxModelFilterSet):
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='devices',
        queryset=Device.objects.all(),
        label=_('Device (ID)'),
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='devices__name',
        queryset=Device.objects.all(),
        to_field_name='name',
        label=_('Device (name)'),
    )
    vm_id = django_filters.ModelMultipleChoiceFilter(
        field_name='vms',
        queryset=VirtualMachine.objects.all(),
        label=_('Virtual Machine (ID)'),
    )
    vm = django_filters.ModelMultipleChoiceFilter(
        field_name='vms__name',
        queryset=VirtualMachine.objects.all(),
        to_field_name='name',
        label=_('Virtual Machine (name)'),
    )
    usergroup_id = django_filters.ModelMultipleChoiceFilter(
        field_name='user_groups',
        queryset=UserGroup.objects.all(),
        label=_('User Group (ID)'),
    )
    usergroup = django_filters.ModelMultipleChoiceFilter(
        field_name='user_groups__name',
        queryset=UserGroup.objects.all(),
        to_field_name='name',
        label=_('User Group (name)'),
    )

    class Meta:
        model = DeviceGroup
        fields = ('id', 'name', 'description')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(comments__icontains=value)
        )


class UserGroupFilterSet(NetBoxModelFilterSet):
    contact_id = django_filters.ModelMultipleChoiceFilter(
        field_name='contacts',
        queryset=Contact.objects.all(),
        label=_('Contact (ID)'),
    )
    contact = django_filters.ModelMultipleChoiceFilter(
        field_name='contacts__name',
        queryset=Contact.objects.all(),
        to_field_name='name',
        label=_('Contact (name)'),
    )
    devicegroup_id = django_filters.ModelMultipleChoiceFilter(
        field_name='devicegroups',
        queryset=DeviceGroup.objects.all(),
        label=_('Device Group (ID)'),
    )
    devicegroup = django_filters.ModelMultipleChoiceFilter(
        field_name='devicegroups__name',
        queryset=DeviceGroup.objects.all(),
        to_field_name='name',
        label=_('Device Group (name)'),
    )

    class Meta:
        model = UserGroup
        fields = ('id', 'name', 'description')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(comments__icontains=value)
        )
