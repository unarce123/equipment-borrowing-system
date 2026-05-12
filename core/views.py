from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from equipment.models import Equipment
from borrow.models import BorrowRequest

@login_required
def dashboard(request):

    context = {
        'total_equipment': Equipment.objects.count(),
        'available_equipment': Equipment.objects.filter(quantity__gt=0).count(),
        'pending_requests': BorrowRequest.objects.filter(status='pending').count(),
        'approved_requests': BorrowRequest.objects.filter(status='approved').count(),
    }

    return render(request, 'core/dashboard.html', context)