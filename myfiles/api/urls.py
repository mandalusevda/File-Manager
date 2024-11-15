from django.urls import (
    path, 
    include,
    re_path
)
from rest_framework import routers
from rest_framework_simplejwt import views

from .views import (
    FolderViewSet,
    FileViewSet
)
from .auth_views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView
)

router = routers.DefaultRouter()
router.register("folders", FolderViewSet, basename="folder")
router.register("files", FileViewSet, basename="file")


urlpatterns = (
    path('', include(router.urls)),
    re_path(r"^create/?", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    re_path(r"^refresh/?", CustomTokenRefreshView.as_view(), name="jwt-refresh"),
    re_path(r"^verify/?", CustomTokenVerifyView.as_view(), name="jwt-verify"),
)