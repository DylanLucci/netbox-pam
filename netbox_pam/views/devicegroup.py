from virtualization.filtersets import VirtualMachineFilterSet
from virtualization.models import VirtualMachine
from virtualization.tables import VirtualMachineTable

from dcim.filtersets import DeviceFilterSet
from dcim.models import Device
from dcim.tables import DeviceTable
from netbox.views import generic
from utilities.views import GetRelatedModelsMixin, ViewTab, register_model_view

from .. import filtersets, forms, models, tables

__all__ = (
    'DeviceGroupView',
    'DeviceGroupListView',
    'DeviceGroupEditView',
    'DeviceGroupDeleteView',
    'DeviceGroupBulkEditView',
    'DeviceGroupBulkImportView',
    'DeviceGroupBulkDeleteView',
    'DeviceGroupDevicesView',
    'DeviceGroupVirtualMachinesView',
)


@register_model_view(models.DeviceGroup)
class DeviceGroupView(generic.ObjectView, GetRelatedModelsMixin):
    queryset = models.DeviceGroup.objects.all()

    def get_extra_context(self, request, instance):
        return {
            'related_models': self.get_related_models(request, instance),
        }


@register_model_view(models.DeviceGroup, 'list', path='', detail=False)
class DeviceGroupListView(generic.ObjectListView):
    queryset = models.DeviceGroup.objects.all()
    table = tables.DeviceGroupTable
    filterset = filtersets.DeviceGroupFilterSet
    filterset_form = forms.DeviceGroupFilterForm


@register_model_view(models.DeviceGroup, 'edit')
@register_model_view(models.DeviceGroup, 'add', detail=False)
class DeviceGroupEditView(generic.ObjectEditView):
    queryset = models.DeviceGroup.objects.all()
    form = forms.DeviceGroupForm


@register_model_view(models.DeviceGroup, 'delete')
class DeviceGroupDeleteView(generic.ObjectDeleteView):
    queryset = models.DeviceGroup.objects.all()


@register_model_view(models.DeviceGroup, 'bulk_edit', path='edit', detail=False)
class DeviceGroupBulkEditView(generic.BulkEditView):
    queryset = models.DeviceGroup.objects.all()
    filterset = filtersets.DeviceGroupFilterSet
    table = tables.DeviceGroupTable
    form = forms.DeviceGroupBulkEditForm


@register_model_view(models.DeviceGroup, 'bulk_import', path='import', detail=False)
class DeviceGroupBulkImportView(generic.BulkImportView):
    queryset = models.DeviceGroup.objects.all()
    model_form = forms.DeviceGroupImportForm


@register_model_view(models.DeviceGroup, 'bulk_delete', path='delete', detail=False)
class DeviceGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = models.DeviceGroup.objects.all()
    filterset = filtersets.DeviceGroupFilterSet
    table = tables.DeviceGroupTable


@register_model_view(models.DeviceGroup, name='devices')
class DeviceGroupDevicesView(generic.ObjectChildrenView):
    template_name = 'netbox_pam/devicegroup_devices.html'
    queryset = models.DeviceGroup.objects.all()
    child_model = Device
    table = DeviceTable
    filterset = DeviceFilterSet
    tab = ViewTab(
        label='Assigned Devices',
        badge=lambda obj: Device.objects.filter(device_groups=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(device_groups=parent)


@register_model_view(models.DeviceGroup, name='vms')
class DeviceGroupVirtualMachinesView(generic.ObjectChildrenView):
    template_name = 'netbox_pam/devicegroup_vms.html'
    queryset = models.DeviceGroup.objects.all()
    child_model = VirtualMachine
    table = VirtualMachineTable
    filterset = VirtualMachineFilterSet
    tab = ViewTab(
        label='Assigned Virtual Machines',
        badge=lambda obj: VirtualMachine.objects.filter(device_groups=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(device_groups=parent)
