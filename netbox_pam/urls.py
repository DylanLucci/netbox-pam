from django.urls import include, path

from utilities.urls import get_model_urls

from . import views

urlpatterns = [
    path('device-groups/', include(get_model_urls('netbox_pam', 'devicegroup', detail=False))),
    path('device-groups/<int:pk>/', include(get_model_urls('netbox_pam', 'devicegroup'))),
    path(
        'device-groups/<int:pk>/devices/',
        views.DeviceGroupDevicesView.as_view(), name='devicegroup_devices'
    ),
    path(
        'device-groups/<int:pk>/virtual-machines/',
        views.DeviceGroupVirtualMachinesView.as_view(), name='devicegroup_vms'
    ),
    path('user-groups/', include(get_model_urls('netbox_pam', 'usergroup', detail=False))),
    path('user-groups/<int:pk>/', include(get_model_urls('netbox_pam', 'usergroup'))),
    path(
        'user-groups/<int:pk>/contacts/',
        views.UserGroupContactsView.as_view(), name='usergroup_contacts'
    ),

    path('sync/', views.JumpcloudSyncView.as_view(), name='jumpcloud_sync'),
]
