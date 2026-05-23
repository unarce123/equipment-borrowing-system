from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from equipment.models import Equipment
from borrow.models import BorrowRequest


@login_required
def dashboard(request):

    today = timezone.now().date()

    # REMOVE ALL RETURNED ITEMS FIRST (MAIN FIX)
    active_borrows = BorrowRequest.objects.filter(
        user=request.user
    ).exclude(status='returned')

    # DUE TODAY (only active + approved)
    due_today = active_borrows.filter(
        status='approved',
        return_date=today
    ).exists()

    # OVERDUE (only active + approved)
    overdue_items = active_borrows.filter(
        status='approved',
        return_date__lt=today
    ).exists()

    context = {

        # INVENTORY
        'total_equipment': Equipment.objects.count(),

        'available_equipment': Equipment.objects.filter(
            quantity__gt=0
        ).count(),

        # REQUEST COUNTS
        'pending_requests': BorrowRequest.objects.filter(
            status='pending'
        ).count(),

        'approved_requests': BorrowRequest.objects.filter(
            status='approved'
        ).count(),

        'returned_requests': BorrowRequest.objects.filter(
            status='returned'
        ).count(),

        # ALERTS (FIXED)
        'due_today': due_today,
        'overdue_items': overdue_items,
    }

    return render(request, 'core/dashboard.html', context)