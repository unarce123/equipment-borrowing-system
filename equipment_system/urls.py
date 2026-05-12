from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Equipment Management System"
admin.site.site_title = "Equipment Admin Portal"
admin.site.index_title = "Welcome to Equipment System Admin"

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('equipment/', include('equipment.urls')),
    path('borrow/', include('borrow.urls')),
]