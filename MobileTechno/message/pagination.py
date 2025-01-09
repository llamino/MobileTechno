# messaging/pagination.py

from rest_framework.pagination import PageNumberPagination

class MessagingPagination(PageNumberPagination):
    page_size = 10  # تعداد آیتم‌ها در هر صفحه
    page_size_query_param = 'page_size'  # امکان تغییر page_size از طریق پارامتر URL
    max_page_size = 100  # حداکثر تعداد آیتم‌ها در هر صفحه
