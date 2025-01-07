# mobile/views.py
from rest_framework import viewsets, permissions, status
from .models import Mobile
from .pagination import MobilePagination
from .serializers import MobileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from bs4 import BeautifulSoup

from accounts.models import UserRequest  # فرض بر وجود مدل UserRequest

class MobileViewSet(viewsets.ModelViewSet):
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['price']
    ordering_fields = ['price', 'created_at']
    pagination_class = MobilePagination

    def list(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        if user:
            user_request, created = UserRequest.objects.get_or_create(user=user)
            user_request.reset_requests_if_needed()
            if user_request.requests_today >= 3:
                return Response({"detail": "حداکثر تعداد پیشنهادات شما به ۳ رسید."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            user_request.requests_today += 1
            user_request.save()
        else:
            # محدودیت برای مهمان‌ها
            guest_requests = request.session.get('guest_requests', 0)
            if guest_requests >= 1:
                return Response({"detail": "حداکثر تعداد پیشنهادات برای مهمان‌ها یک است."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            request.session['guest_requests'] = guest_requests + 1

        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def get_price(self, request, pk=None):
        mobile = self.get_object()
        price = self.get_price_from_techonolife(mobile.url)
        if price:
            mobile.price = price
            mobile.save()
            return Response({"price": price})
        return Response({"detail": "قیمت یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

    def get_price_from_techonolife(self, mobile_url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            response = requests.get(mobile_url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # بسته به ساختار HTML تکنولایف، عنصر قیمت را پیدا کنید
                price_element = soup.find('span', class_='price')  # باید به ساختار واقعی HTML مراجعه کنید
                if price_element:
                    price_text = price_element.get_text().strip()
                    # پردازش متن قیمت به عدد
                    price = float(price_text.replace(',', '').replace('تومان', ''))
                    return price
        except Exception as e:
            print(f"Error fetching price: {e}")
        return None
