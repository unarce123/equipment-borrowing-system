from django.contrib import admin
from .models import BorrowRequest


@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    search_fields = ("user__username", "equipment__name", "status")

    list_filter = (
        "status",        
        "borrow_date",   
        "return_date",   
    )