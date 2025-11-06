from netbox.views import generic
from tenancy.filtersets import ContactFilterSet
from tenancy.models import Contact
from tenancy.tables import ContactTable
from utilities.views import GetRelatedModelsMixin, ViewTab, register_model_view

from .. import filtersets, forms, models, tables

__all__ = (
    'UserGroupView',
    'UserGroupListView',
    'UserGroupEditView',
    'UserGroupDeleteView',
    'UserGroupBulkEditView',
    'UserGroupBulkImportView',
    'UserGroupBulkDeleteView',
    'UserGroupContactsView',
)


@register_model_view(models.UserGroup)
class UserGroupView(generic.ObjectView, GetRelatedModelsMixin):
    queryset = models.UserGroup.objects.all()

    def get_extra_context(self, request, instance):
        return {
            'related_models': self.get_related_models(request, instance),
        }


@register_model_view(models.UserGroup, 'list', path='', detail=False)
class UserGroupListView(generic.ObjectListView):
    queryset = models.UserGroup.objects.all()
    table = tables.UserGroupTable
    filterset = filtersets.UserGroupFilterSet
    filterset_form = forms.UserGroupFilterForm


@register_model_view(models.UserGroup, 'edit')
@register_model_view(models.UserGroup, 'add', detail=False)
class UserGroupEditView(generic.ObjectEditView):
    queryset = models.UserGroup.objects.all()
    form = forms.UserGroupForm


@register_model_view(models.UserGroup, 'delete')
class UserGroupDeleteView(generic.ObjectDeleteView):
    queryset = models.UserGroup.objects.all()


@register_model_view(models.UserGroup, 'bulk_edit', path='edit', detail=False)
class UserGroupBulkEditView(generic.BulkEditView):
    queryset = models.UserGroup.objects.all()
    filterset = filtersets.UserGroupFilterSet
    table = tables.UserGroupTable
    form = forms.UserGroupBulkEditForm


@register_model_view(models.UserGroup, 'bulk_import', path='import', detail=False)
class UserGroupBulkImportView(generic.BulkImportView):
    queryset = models.UserGroup.objects.all()
    model_form = forms.UserGroupImportForm


@register_model_view(models.UserGroup, 'bulk_delete', path='delete', detail=False)
class UserGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = models.UserGroup.objects.all()
    filterset = filtersets.UserGroupFilterSet
    table = tables.UserGroupTable


@register_model_view(models.UserGroup, name='contacts')
class UserGroupContactsView(generic.ObjectChildrenView):
    template_name = 'netbox_pam/usergroup_contacts.html'
    queryset = models.UserGroup.objects.all()
    child_model = Contact
    table = ContactTable
    filterset = ContactFilterSet
    tab = ViewTab(
        label='Assigned Contacts',
        badge=lambda obj: Contact.objects.filter(user_groups=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(user_groups=parent)
