# mobile/admin.py
from django.contrib import admin
from .models import Mobile

@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'added_time')
    search_fields = ('name',)