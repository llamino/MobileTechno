import os
from celery import Celery
from django.conf import settings

# تنظیم متغیر محیطی برای تنظیمات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MobileTechno.settings')

# ایجاد یک نمونه از Celery
app = Celery('MobileTechno')

# استفاده از تنظیمات Django برای Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# جستجوی خودکار تسک‌ها در اپلیکیشن‌های Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.broker_connection_retry_on_startup = True


