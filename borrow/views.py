from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import BorrowRequest
from .forms import BorrowRequestForm
from equipment.models import Equipment
from accounts.utils import is_admin


# ------------------------
# BORROW LIST
# ------------------------
@login_required
def borrow_list(request):

    if request.user.is_superuser:
        requests = BorrowRequest.objects.all()
    else:
        requests = BorrowRequest.objects.filter(user=request.user)

    return render(request, 'borrow/list.html', {'requests': requests})


# ------------------------
# CREATE BORROW
# ------------------------
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


# ------------------------
# APPROVE (ADMIN)
# ------------------------
@login_required
@user_passes_test(is_admin)
def approve_borrow(request, pk):

    borrow = get_object_or_404(BorrowRequest, pk=pk)

    if borrow.status != 'pending':
        return redirect('borrow_list')

    equipment = borrow.equipment

    # CHECK STOCK
    if borrow.quantity > equipment.quantity:
        messages.error(request, "Not enough stock available")
        return redirect('borrow_list')

    # REDUCE STOCK
    equipment.quantity -= borrow.quantity
    equipment.save()

    # FORCE STATUS SYNC
    equipment.refresh_from_db()
    equipment.save()

    borrow.status = 'approved'
    borrow.save()

    messages.success(request, "Borrow request approved")

    return redirect('borrow_list')


# ------------------------
# REJECT (ADMIN)
# ------------------------
@login_required
@user_passes_test(is_admin)
def reject_borrow(request, pk):

    borrow = get_object_or_404(BorrowRequest, pk=pk)

    if borrow.status == 'pending':
        borrow.status = 'rejected'
        borrow.save()

        messages.success(request, "Borrow request rejected")

    return redirect('borrow_list')


# ------------------------
# RETURN ITEM (USER OR ADMIN)
# ------------------------
@login_required
def return_borrow(request, pk):

    borrow = get_object_or_404(BorrowRequest, pk=pk)

    if borrow.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden()

    if borrow.status != 'approved':
        return redirect('borrow_list')

    equipment = borrow.equipment

    # RESTORE STOCK
    equipment.quantity += borrow.quantity
    equipment.save()

    # FORCE STATUS SYNC
    equipment.refresh_from_db()
    equipment.save()

    borrow.status = 'returned'
    borrow.save()

    messages.success(request, "Equipment returned successfully")

    return redirect('borrow_list')


# ------------------------
# CANCEL REQUEST
# ------------------------
@login_required
def delete_borrow(request, pk):

    borrow = get_object_or_404(BorrowRequest, pk=pk)

    if borrow.user != request.user:
        return HttpResponseForbidden()

    if borrow.status == 'pending':
        borrow.delete()
        messages.success(request, "Borrow request cancelled")

    return redirect('borrow_list')