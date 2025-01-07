from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile

#---------------------------begin Inline classes-----------------------------------------------


#--------------------------end Inline classes-----------------------------------------------------






#--------------------------begin custom user admin classes-----------------------------------------------------



class UserAdmin(BaseUserAdmin):
    # Fields to be displayed in the admin list view
    list_display = ('email', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'phone_number')
    ordering = ('email',)

    # Fields in detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('phone_number',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'create_date', 'update_date')}),
    )

    # Fields displayed when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # def has_delete_permission(self, request, obj=None):
    #     return True  # اجازه حذف را فعال می‌کند

    # Readonly fields
    readonly_fields = ('create_date', 'update_date')

    # Add AddressInline to UserAdmin

# Register the custom User model
admin.site.register(User, UserAdmin)

#--------------------------end of custom user admin classes-----------------------------------------------------



#--------------------------begin admin classes------------------------------------------------

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')
    search_fields = ('user__email', 'first_name', 'last_name')
    ordering = ('user__email',)


#---------------------------end of admin classes-----------------------------------