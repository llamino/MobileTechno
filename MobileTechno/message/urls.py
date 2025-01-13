# message/urls.py
from django.urls import path
from .views import (
    ListUsersAPIView,
    UserMessageHistoryAPIView,
    SendMessageAPIView,
    MessageListAPIView,
    MessageDetailAPIView,
    DeleteSentMessagesAPIView,
    DeleteAllMessagesAPIView,
    DeleteMessageAPIView
)

urlpatterns = [
    path('list_users/', ListUsersAPIView.as_view(), name='list-users'),
    path('history/<str:username>/', UserMessageHistoryAPIView.as_view(), name='user-message-history'),
    path('send_message/', SendMessageAPIView.as_view(), name='send-message'),
    path('list_messages/', MessageListAPIView.as_view(), name='message-list'),
    path('detail_message/<int:pk>/', MessageDetailAPIView.as_view(), name='message-detail'),
    path('delete_message/<int:pk>/', DeleteMessageAPIView.as_view(), name='delete-message'),
    path('delete_messages_sent/<str:username>/', DeleteSentMessagesAPIView.as_view(), name='delete-sent-messages'),
    path('delete_message_all/<str:username>/', DeleteAllMessagesAPIView.as_view(), name='delete-all-messages'),
]
