# message/urls.py
from django.urls import path
from .views import (
    ListUsersAPIView,
    UserMessageHistoryAPIView,
    SendMessageAPIView,
    MessageListAPIView,
    MessageDetailAPIView,
    DeleteSentMessagesAPIView,
    DeleteAllMessagesAPIView
)

urlpatterns = [
    path('messages/users/', ListUsersAPIView.as_view(), name='list-users'),
    path('messages/user/<str:username>/history/', UserMessageHistoryAPIView.as_view(), name='user-message-history'),
    path('messages/send/', SendMessageAPIView.as_view(), name='send-message'),
    path('messages/', MessageListAPIView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageDetailAPIView.as_view(), name='message-detail'),
    path('messages/user/<str:username>/delete_sent/', DeleteSentMessagesAPIView.as_view(), name='delete-sent-messages'),
    path('messages/user/<str:username>/delete_all/', DeleteAllMessagesAPIView.as_view(), name='delete-all-messages'),
]
