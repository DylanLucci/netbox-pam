from netbox.api.routers import NetBoxRouter
from . import views

router = NetBoxRouter()

router.register('device-groups', views.DeviceGroupViewSet)
router.register('user-groups', views.UserGroupViewSet)

urlpatterns = router.urls
