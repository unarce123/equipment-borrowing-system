from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile


class CustomUserAdmin(BaseUserAdmin):
    filter_vertical = ("user_permissions", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    list_filter = () 


class CustomGroupAdmin(admin.ModelAdmin):
    filter_vertical = ("permissions",)
    search_fields = ("name",)
    list_filter = () 


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ("user__username", "user__email")
    list_filter = () 


# Replace default admin
admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)
admin.site.register(UserProfile, UserProfileAdmin)