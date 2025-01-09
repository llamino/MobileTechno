from django.urls import path
from .views import MessageListCreateView, UserMessagesView, MessageDetailView

urlpatterns = [
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('messages/user/<str:username>/', UserMessagesView.as_view(), name='user-messages'),
]
