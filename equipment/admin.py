from django.contrib import admin
from .models import Equipment, Category


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):

    # SEARCH BAR
    search_fields = ("name", "category__name", "description")

    # FILTER SIDEBAR
    list_filter = ("category",)

    # PAGINATION
    list_per_page = 10

    # cleaner ordering newest first
    ordering = ("-id",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    # SEARCH BAR
    search_fields = ("name",)

    # NO FILTER NEEDED
    list_filter = ()