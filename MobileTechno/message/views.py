# message/views.py
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth.models import User

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(receiver=user).order_by('-timestamp')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

# افزودن ویو برای قالب وب
from django.contrib.auth.decorators import login_required

@login_required
def message_page(request):
    return render(request, 'message/message.html')
