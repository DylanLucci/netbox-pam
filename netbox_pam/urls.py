from django.urls import path

from . import views

urlpatterns = [
    path('sync/', views.JumpcloudSyncView.as_view(), name='jumpcloud_sync'),
]
