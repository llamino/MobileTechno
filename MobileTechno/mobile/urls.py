# message/urls.py
from django.urls import path
from .views import MobileListAPIView, MobileDetailAPIView, MobileSuggestedAPIView

urlpatterns = [
    path('mobile_list/', MobileListAPIView.as_view(), name='mobile-list'),
    path('mobile_detail/<str:product_id>/', MobileDetailAPIView.as_view(), name='mobile-detail'),
    path('mobile_suggested/', MobileSuggestedAPIView.as_view(), name='mobile-suggested'),
]
