from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Equipment, Category

admin.site.register(Equipment)
admin.site.register(Category)
