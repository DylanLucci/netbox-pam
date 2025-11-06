from netbox.api.viewsets import NetBoxModelViewSet

from ..models import DeviceGroup, UserGroup
from .serializers import DeviceGroupSerializer, UserGroupSerializer


class DeviceGroupViewSet(NetBoxModelViewSet):
    queryset = DeviceGroup.objects.prefetch_related('devices', 'vms', 'tags')
    serializer_class = DeviceGroupSerializer


class UserGroupViewSet(NetBoxModelViewSet):
    queryset = UserGroup.objects.prefetch_related('contacts', 'devicegroups', 'tags')
    serializer_class = UserGroupSerializer
