from django.urls import path, include
from rest_framework import routers
from .views import MobileViewSet

router = routers.DefaultRouter()
router.register(r'mobiles', MobileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
