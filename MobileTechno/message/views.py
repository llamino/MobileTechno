# message/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Message, User
from .serializers import MessageSerializer, UserSerializer
from django.db import models
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .pagination import MessagingPagination

class ListUsersAPIView(APIView):
    """
    APIView برای لیست کردن همه کاربران که کاربر فعلی با آنها پیام داده یا دریافت کرده است.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="لیست کردن همه کاربران که با آنها پیام داده یا دریافت کرده‌اید.",
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request):
        """
        دریافت لیست کاربران مرتبط.
        """
        sent_users = User.objects.filter(sent_messages__sender=request.user).distinct()
        received_users = User.objects.filter(received_messages__recipient=request.user).distinct()
        users = (sent_users | received_users).distinct()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserMessageHistoryAPIView(APIView):
    """
    APIView برای نمایش تاریخچه پیام‌های ارسال شده و دریافت شده با یک کاربر مشخص.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = MessagingPagination

    @swagger_auto_schema(
        operation_description="نمایش تاریخچه پیام‌ها با کاربر مشخص شده.",
        manual_parameters=[
            openapi.Parameter(
                'username',
                openapi.IN_PATH,
                description="نام کاربری کاربر مورد نظر",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: MessageSerializer(many=True),
            404: 'User not found.'
        }
    )
    def get(self, request, username):
        """
        نمایش تاریخچه پیام‌های ارسال شده و دریافت شده با یک کاربر مشخص.
        """
        try:
            other_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        messages = Message.objects.filter(
            (models.Q(sender=request.user) & models.Q(recipient=other_user)) |
            (models.Q(sender=other_user) & models.Q(recipient=request.user))
        ).order_by('-timestamp')

        paginator = MessagingPagination()
        page = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)



class SendMessageAPIView(APIView):
    serializer_class = MessageSerializer
    """
    APIView برای ارسال پیام به یک کاربر مشخص.
    """
    permission_classes = [IsAuthenticated]


    authorization_header = openapi.Parameter(
        'Authorization',
        openapi.IN_HEADER,
        description="توکن JWT با پیشوند Bearer",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(
        operation_description="ارسال پیام به کاربر مشخص شده.",
        request_body=MessageSerializer,
        responses={
            201: MessageSerializer(),
            400: 'Bad Request',
            404: 'User not found.'
        },
        manual_parameters=[authorization_header])

    def post(self, request):
        """
        ارسال پیام.
        """
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            recipient_username = serializer.validated_data.get('recipient').username
            if recipient_username == request.user.username:
                return Response({'detail': 'Cannot send message to yourself.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageListAPIView(APIView):
    """
    APIView برای نمایش لیست پیام‌های کاربر فعلی.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = MessagingPagination

    @swagger_auto_schema(
        operation_description="نمایش لیست پیام‌های ارسال شده و دریافت شده توسط کاربر فعلی.",
        responses={200: MessageSerializer(many=True)}
    )
    def get(self, request):
        """
        دریافت لیست پیام‌ها.
        """
        messages = Message.objects.filter(
            models.Q(sender=request.user) | models.Q(recipient=request.user)
        ).order_by('-timestamp')

        paginator = MessagingPagination()
        page = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="ارسال پیام جدید.",
        request_body=MessageSerializer,
        responses={
            201: MessageSerializer(),
            400: 'Bad Request'
        }
    )
    def post(self, request):
        """
        ارسال پیام جدید.
        """
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            recipient_username = serializer.validated_data.get('recipient').username
            if recipient_username == request.user.username:
                return Response({'detail': 'Cannot send message to yourself.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDetailAPIView(APIView):
    """
    APIView برای مشاهده جزئیات یک پیام خاص و علامت‌گذاری آن به عنوان خوانده شده.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="مشاهده جزئیات یک پیام خاص و علامت‌گذاری آن به عنوان خوانده شده.",
        responses={
            200: MessageSerializer(),
            404: 'Not found.'
        }
    )
    def get(self, request, pk):
        """
        دریافت جزئیات پیام.
        """
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        if message.recipient != request.user and message.sender != request.user:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        # علامت‌گذاری پیام به عنوان خوانده شده
        if message.recipient == request.user and not message.is_read:
            message.is_read = True
            message.save()

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="حذف یک پیام خاص که توسط شما ارسال شده است.",
        responses={
            204: 'No Content',
            403: 'Forbidden',
            404: 'Not found.'
        }
    )
    def delete(self, request, pk):
        """
        حذف پیام.
        """
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        if message.sender != request.user:
            return Response({'detail': 'Forbidden.'}, status=status.HTTP_403_FORBIDDEN)

        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteSentMessagesAPIView(APIView):
    """
    APIView برای حذف همه پیام‌هایی که توسط کاربر فعلی به یک کاربر مشخص ارسال شده‌اند.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="حذف پیام‌هایی که توسط شما به کاربر مشخص شده ارسال شده‌اند.",
        manual_parameters=[
            openapi.Parameter(
                'username',
                openapi.IN_PATH,
                description="نام کاربری کاربر مورد نظر",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            204: 'No Content',
            404: 'User not found.'
        }
    )
    def delete(self, request, username):
        """
        حذف پیام‌های ارسال شده به یک کاربر.
        """
        try:
            recipient = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        deleted_count, _ = Message.objects.filter(sender=request.user, recipient=recipient).delete()
        return Response({'detail': f'Deleted {deleted_count} messages sent to {username}.'}, status=status.HTTP_204_NO_CONTENT)


class DeleteAllMessagesAPIView(APIView):
    """
    APIView برای حذف همه پیام‌های بین کاربر فعلی و یک کاربر مشخص.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="حذف همه پیام‌های بین شما و کاربر مشخص شده.",
        manual_parameters=[
            openapi.Parameter(
                'username',
                openapi.IN_PATH,
                description="نام کاربری کاربر مورد نظر",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            204: 'No Content',
            404: 'User not found.'
        }
    )
    def delete(self, request, username):
        """
        حذف همه پیام‌های با یک کاربر.
        """
        try:
            other_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        deleted_count, _ = Message.objects.filter(
            models.Q(sender=request.user, recipient=other_user) |
            models.Q(sender=other_user, recipient=request.user)
        ).delete()
        return Response({'detail': f'Deleted {deleted_count} messages with {username}.'}, status=status.HTTP_204_NO_CONTENT)
