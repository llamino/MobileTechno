from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Mobile  # وارد کردن مدل Mobile

class MobileModelTest(TestCase):
    def test_create_mobile(self):
        """
        بررسی می‌کند که یک Mobile به درستی ایجاد شود.
        """
        mobile = Mobile.objects.create(
            product_id=12345,
            name='Test Mobile',
            image_url='http://example.com/image.jpg',
            price=299.99,
            cpu='Test CPU',
            memory='64GB',
            ram='4GB',
            monitor_size='6.1 inches',
            back_camera='12MP',
            battery='3000mAh'
        )
        self.assertEqual(mobile.name, 'Test Mobile')
        self.assertEqual(mobile.price, 299.99)
        self.assertTrue(Mobile.objects.filter(product_id=12345).exists())

class MobileAPITest(APITestCase):
    def setUp(self):
        """
        ایجاد یک موبایل برای استفاده در تست‌ها.
        """
        self.mobile = Mobile.objects.create(
            product_id=54321,
            name='Sample Mobile',
            image_url='http://example.com/sample.jpg',
            price=399.99,
            cpu='Sample CPU',
            memory='128GB',
            ram='6GB',
            monitor_size='6.5 inches',
            back_camera='16MP',
            battery='4000mAh'
        )

    def test_mobile_list_api(self):
        """
        بررسی می‌کند که API لیست موبایل‌ها به درستی کار می‌کند.
        """
        url = reverse('mobile-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # بررسی اینکه حداقل یک موبایل در نتایج وجود دارد
        self.assertTrue(len(response.data['results']) >= 1)

    def test_mobile_detail_api_success(self):
        """
        بررسی می‌کند که API جزئیات موبایل با product_id معتبر به درستی کار می‌کند.
        """
        url = reverse('mobile-detail', args=[self.mobile.product_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Sample Mobile')

    def test_mobile_detail_api_not_found(self):
        """
        بررسی می‌کند که API جزئیات موبایل با product_id نامعتبر، 404 برگرداند.
        """
        url = reverse('mobile-detail', args=[99999])  # فرض بر این است که این product_id وجود ندارد
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
