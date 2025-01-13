# mobile/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import filters
from .models import Mobile
from .serializers import MobileListSerializer, MobileDetailSerializer
from .pagination import MobilePagination
from accounts.models import UserRequest
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class MobileListAPIView(APIView):
    """
    API view to list all mobiles with name, price, and image.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = MobileListSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of all mobiles with name, price, and image.",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of items per page", type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request):
        mobiles = Mobile.objects.all().order_by('-added_time')
        paginator = MobilePagination()
        paginated_mobiles = paginator.paginate_queryset(mobiles, request)
        serializer = self.serializer_class(paginated_mobiles, many=True)
        return paginator.get_paginated_response(serializer.data)



class MobileDetailAPIView(APIView):
    """
    API view to retrieve details of a mobile by its product ID.
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve details of a mobile by product ID.",
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_PATH, description="Product ID of the mobile", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, product_id, format=None):
        try:
            mobile = Mobile.objects.get(product_id=product_id)
        except Mobile.DoesNotExist:
            return Response({"detail": "Mobile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MobileDetailSerializer(mobile)
        return Response(serializer.data, status=status.HTTP_200_OK)



class MobileSuggestedAPIView(APIView):
    """
    API view to suggest mobiles based on price range and added time with rate limiting.
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Get suggested mobiles based on price range and added time. Rate limited based on user authentication.",
        manual_parameters=[
            openapi.Parameter('price__gte', openapi.IN_QUERY, description="Minimum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('price__lte', openapi.IN_QUERY, description="Maximum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('added_time__gte', openapi.IN_QUERY, description="Added after date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('added_time__lte', openapi.IN_QUERY, description="Added before date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of items per page", type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            user_request, created = UserRequest.objects.get_or_create(user=user)
            user_request.reset_requests_if_needed()
            if user_request.requests_today >= 3:
                return Response({"detail": "You have reached the maximum number of suggestions for today."},
                                status=status.HTTP_429_TOO_MANY_REQUESTS)
            user_request.requests_today += 1
            user_request.last_request = timezone.now()
            user_request.save()
        else:
            # برای کاربران میهمان، از session-based tracking استفاده می‌کنیم
            session = request.session
            if 'guest_requests_today' not in session:
                session['guest_requests_today'] = 0
            if session['guest_requests_today'] >= 1:
                return Response({"detail": "You have reached the maximum number of suggestions for today."},
                                status=status.HTTP_429_TOO_MANY_REQUESTS)
            session['guest_requests_today'] += 1
            session.modified = True

        # دریافت پارامترهای فیلتر
        price_gte = request.GET.get('price__gte')
        price_lte = request.GET.get('price__lte')
        added_time_gte = request.GET.get('added_time__gte')
        added_time_lte = request.GET.get('added_time__lte')

        mobiles = Mobile.objects.all()

        if price_gte:
            mobiles = mobiles.filter(price__gte=price_gte)
        if price_lte:
            mobiles = mobiles.filter(price__lte=price_lte)
        if added_time_gte:
            mobiles = mobiles.filter(added_time__gte=added_time_gte)
        if added_time_lte:
            mobiles = mobiles.filter(added_time__lte=added_time_lte)

        mobiles = mobiles.order_by('-added_time')

        paginator = MobilePagination()
        paginated_mobiles = paginator.paginate_queryset(mobiles, request)
        serializer = MobileListSerializer(paginated_mobiles, many=True)
        return paginator.get_paginated_response(serializer.data)
