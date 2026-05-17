from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from equipment.models import Equipment
from borrow.models import BorrowRequest


@login_required
def dashboard(request):

    today = timezone.now().date()

    # USER NOTIFICATIONS
    due_today = BorrowRequest.objects.filter(
        user=request.user,
        return_date=today,
        status='approved'
    )

    overdue_items = BorrowRequest.objects.filter(
        user=request.user,
        return_date__lt=today,
        status='approved'
    )

    context = {

        'total_equipment': Equipment.objects.count(),

        'available_equipment': Equipment.objects.filter(
            quantity__gt=0
        ).count(),

        'pending_requests': BorrowRequest.objects.filter(
            status='pending'
        ).count(),

        'approved_requests': BorrowRequest.objects.filter(
            status='approved'
        ).count(),

        'returned_requests': BorrowRequest.objects.filter(
            status='returned'
        ).count(),

        # NOTIFICATIONS
        'due_today': due_today,
        'overdue_items': overdue_items,
    }

    return render(request, 'core/dashboard.html', context)