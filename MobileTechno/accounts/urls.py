# accounts/urls.py

from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    # صفحات وب
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),

    # API URLs
    path('api/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', views.CustomTokenObtainPairView.as_view(), name='api_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
]
