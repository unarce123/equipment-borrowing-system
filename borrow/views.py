from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import BorrowRequest
from .forms import BorrowRequestForm
from equipment.models import Equipment
from accounts.utils import is_admin


@login_required
def borrow_list(request):
    if request.user.is_superuser:
        requests = BorrowRequest.objects.all()
    else:
        requests = BorrowRequest.objects.filter(user=request.user)

    return render(request, 'borrow/list.html', {'requests': requests})


@login_required
def create_borrow(request):
    form = BorrowRequestForm(request.POST or None)

    if form.is_valid():
        borrow = form.save(commit=False)
        borrow.user = request.user
        borrow.status = 'pending'
        borrow.save()

        messages.success(request, "Borrow request submitted successfully")
        return redirect('borrow_list')

    return render(request, 'borrow/form.html', {'form': form})


# ADMIN ONLY
@login_required
@user_passes_test(is_admin)
def approve_borrow(request, pk):
    borrow = get_object_or_404(BorrowRequest, pk=pk)

    if borrow.status == 'pending':
        equipment = borrow.equipment

        if equipment.quantity >= borrow.quantity:
            equipment.quantity -= borrow.quantity
            equipment.save()

            borrow.status = 'approved'
            borrow.save()

            messages.success(request, "Borrow request approved")

    return redirect('borrow_list')


# ADMIN ONLY
@login_required
@user_passes_test(is_admin)
def reject_borrow(request, pk):
    borrow = get_object_or_404(BorrowRequest, pk=pk)

    if borrow.status == 'pending':
        borrow.status = 'rejected'
        borrow.save()

        messages.success(request, "Borrow request rejected")

    return redirect('borrow_list')


@login_required
def return_borrow(request, pk):
    borrow = get_object_or_404(BorrowRequest, pk=pk)

    if borrow.status == 'approved':
        equipment = borrow.equipment
        equipment.quantity += borrow.quantity
        equipment.save()

        borrow.status = 'returned'
        borrow.save()

        messages.success(request, "Equipment returned successfully")

    return redirect('borrow_list')