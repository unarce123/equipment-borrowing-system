from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile


# =========================
# USER ADMIN (VERTICAL PERMISSIONS)
# =========================
class CustomUserAdmin(BaseUserAdmin):
    filter_vertical = ("user_permissions", "groups")


# =========================
# GROUP ADMIN (VERTICAL PERMISSIONS)
# =========================
class CustomGroupAdmin(admin.ModelAdmin):
    filter_vertical = ("permissions",)


# =========================
# UNREGISTER DEFAULTS
# =========================
admin.site.unregister(User)
admin.site.unregister(Group)

# =========================
# REGISTER CUSTOM
# =========================
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)

# YOUR MODEL
admin.site.register(UserProfile)