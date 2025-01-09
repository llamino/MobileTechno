# message/admin.py

from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    پیکربندی نمایش مدل Message در پنل مدیریت Django.
    """
    # فیلدهایی که در لیست نمایش داده می‌شوند
    list_display = ('id', 'sender', 'recipient', 'short_content', 'timestamp', 'is_read')

    # فیلدهایی که قابلیت فیلتر دارند
    list_filter = ('is_read', 'timestamp', 'sender', 'recipient')

    # فیلدهایی که قابلیت جستجو دارند
    search_fields = ('sender__username', 'recipient__username', 'content')

    # فیلدهایی که می‌توانند مرتب‌سازی شوند
    ordering = ('-timestamp',)

    # تعداد کاراکتر نمایش داده شده در لیست پیام‌ها برای فیلد محتوا
    def short_content(self, obj):
        """
        نمایش محتوای پیام به صورت خلاصه در لیست.
        """
        return (obj.content[:75] + '...') if len(obj.content) > 75 else obj.content

    short_content.short_description = 'Content'

    # امکان ویرایش فیلدهای خاص از طریق لیست
    list_editable = ('is_read',)

    # تنظیمات نمایش جزئیات پیام
    readonly_fields = ('sender', 'recipient', 'content', 'timestamp', 'is_read')

    # نمایش فیلدها به صورت مرتب در فرم ویرایش
    fields = ('sender', 'recipient', 'content', 'timestamp', 'is_read')
