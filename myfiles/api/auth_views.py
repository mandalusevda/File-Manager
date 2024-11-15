from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Auth"])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(tags=["Auth"])
class CustomTokenRefreshView(TokenRefreshView):
    pass

@extend_schema(tags=["Auth"])
class CustomTokenVerifyView(TokenVerifyView):
    pass
