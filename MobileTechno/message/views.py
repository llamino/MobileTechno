# message/views.py
from rest_framework import generics, permissions
from .models import Message, User
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .pagination import MessagingPagination  # وارد کردن کلاس صفحه‌بندی

class MessageListCreateView(generics.ListCreateAPIView):
    """
    نمایش لیست پیام‌ها و ارسال پیام جدید.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MessagingPagination  # اعمال صفحه‌بندی

    def get_queryset(self):
        """
        بازگرداندن همه پیام‌ها.
        """
        return Message.objects.all()

    def perform_create(self, serializer):
        """
        تنظیم فرستنده پیام به کاربر فعلی.
        """
        serializer.save(sender=self.request.user)

class UserMessagesView(generics.ListAPIView):
    """
    نمایش پیام‌های ارسال شده و دریافت شده با یک کاربر مشخص.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MessagingPagination  # اعمال صفحه‌بندی

    def get_queryset(self):
        """
        بازگرداندن پیام‌هایی که به یا از کاربر مشخص ارسال شده‌اند.
        """
        username = self.kwargs['username']
        try:
            other_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Message.objects.none()
        return Message.objects.filter(
            (models.Q(sender=self.request.user) & models.Q(recipient=other_user)) |
            (models.Q(sender=other_user) & models.Q(recipient=self.request.user))
        ).order_by('-timestamp')

class MessageDetailView(generics.RetrieveAPIView):
    """
    مشاهده جزئیات یک پیام خاص.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    # صفحه‌بندی برای جزئیات پیام لازم نیست

    def get(self, request, *args, **kwargs):
        message = self.get_object()
        if message.recipient != request.user and message.sender != request.user:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        # علامت‌گذاری پیام به عنوان خوانده شده
        if message.recipient == request.user and not message.is_read:
            message.is_read = True
            message.save()
        return super().get(request, *args, **kwargs)
