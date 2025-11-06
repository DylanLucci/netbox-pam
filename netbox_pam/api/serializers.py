from rest_framework import serializers
from virtualization.api.serializers import VirtualMachineSerializer

from dcim.api.serializers import DeviceSerializer
from tenancy.api.serializers import ContactSerializer
from netbox.api.serializers import NetBoxModelSerializer

from ..models import DeviceGroup, UserGroup


class DeviceGroupSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_pam-api:devicegroup-detail'
    )
    devices = DeviceSerializer(nested=True, many=True)
    vms = VirtualMachineSerializer(nested=True, many=True)

    class Meta:
        model = DeviceGroup
        fields = (
            'id', 'url', 'name', 'display', 'description', 'devices', 'vms', 'comments', 'tags', 'custom_fields',
            'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'name', 'display')


class UserGroupSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_pam-api:usergroup-detail'
    )
    contacts = ContactSerializer(nested=True, many=True)
    devicegroups = DeviceGroupSerializer(nested=True, many=True)

    class Meta:
        model = UserGroup
        fields = (
            'id', 'url', 'name', 'display', 'description', 'contacts', 'devicegroups', 'comments', 'tags',
            'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'name', 'display')
