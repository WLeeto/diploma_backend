from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .custom_jwt.view import MyTokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),

    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/', include('auth_app.urls')),
    path('files/', include('files.urls'))
]
