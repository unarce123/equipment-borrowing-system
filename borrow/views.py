from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from .models import BorrowRequest
from .forms import BorrowRequestForm
from equipment.models import Equipment, Category
from .utils import create_notification


# STAFF + ADMIN ACCESS
def is_staff_or_admin(user):
    return user.is_staff


# BORROW LIST WITH PAGINATION

@login_required
def borrow_list(request):

    if request.user.is_staff:
        requests = BorrowRequest.objects.all()
    else:
        requests = BorrowRequest.objects.filter(user=request.user)

    # SEARCH
    search = request.GET.get('search')
    if search:
        requests = requests.filter(
            user__username__icontains=search
        ) | requests.filter(
            equipment__name__icontains=search
        )

    # STATUS FILTER
    status = request.GET.get('status')
    if status and status != "all":
        requests = requests.filter(status=status)

    # PAGINATION
    paginator = Paginator(requests.order_by('-id'), 10)
    page_number = request.GET.get('page')
    requests = paginator.get_page(page_number)

    return render(request, 'borrow/list.html', {
        'requests': requests,
        'search': search,
        'status': status
    })


# CREATE BORROW

@login_required
def create_borrow(request):

    category_id = request.GET.get('category')
    form = BorrowRequestForm()

    if category_id:
        form.fields['equipment'].queryset = Equipment.objects.filter(
            category_id=category_id
        )
    else:
        form.fields['equipment'].queryset = Equipment.objects.all()

    if request.method == 'POST':

        form = BorrowRequestForm(request.POST)
        post_category = request.POST.get('category')

        if post_category:
            form.fields['equipment'].queryset = Equipment.objects.filter(
                category_id=post_category
            )

        if form.is_valid():

            borrow = form.save(commit=False)
            borrow.user = request.user
            borrow.status = 'pending'
            borrow.save()

            create_notification(
                request.user,
                f"Your borrow request for {borrow.equipment.name} has been submitted.",
                "borrow"
            )

            staffs = User.objects.filter(is_staff=True)

            for staff in staffs:
                create_notification(
                    staff,
                    f"{request.user.username} requested {borrow.equipment.name}.",
                    "borrow"
                )

            messages.success(request, "Borrow request submitted successfully")
            return redirect('borrow_list')

    categories = Category.objects.all()

    return render(request, 'borrow/form.html', {
        'form': form,
        'categories': categories,
        'selected_category': category_id
    })


# APPROVE BORROW

@login_required
@user_passes_test(is_staff_or_admin)
def approve_borrow(request, pk):

    borrow = get_object_or_404(BorrowRequest, pk=pk)

    if borrow.status != 'pending':
        return redirect('borrow_list')

    equipment = borrow.equipment

    if borrow.quantity > equipment.quantity:
        messages.error(request, "Not enough stock available")
        return redirect('borrow_list')

    equipment.quantity -= borrow.quantity
    equipment.save()

    borrow.status = 'approved'
    borrow.save()

    create_notification(
        borrow.user,
        f"Your borrow request for {borrow.equipment.name} has been APPROVED.",
        "approval"
    )

    messages.success(request, "Borrow request approved")
    return redirect('borrow_list')


# REJECT BORROW

@login_required
@user_passes_test(is_staff_or_admin)
def reject_borrow(request, pk):

    borrow = get_object_or_404(BorrowRequest, pk=pk)

    if borrow.status == 'pending':
        borrow.status = 'rejected'
        borrow.save()

        create_notification(
            borrow.user,
            f"Your borrow request for {borrow.equipment.name} was REJECTED.",
            "reject"
        )

        messages.success(request, "Borrow request rejected")

    return redirect('borrow_list')


# RETURN BORROW

@login_required
@user_passes_test(is_staff_or_admin)
def return_borrow(request, pk):

    borrow = get_object_or_404(BorrowRequest, pk=pk)

    if borrow.status != 'approved':
        return redirect('borrow_list')

    equipment = borrow.equipment
    equipment.quantity += borrow.quantity
    equipment.save()

    borrow.status = 'returned'
    borrow.save()

    create_notification(
        borrow.user,
        f"Your borrowed equipment ({borrow.equipment.name}) has been marked as RETURNED.",
        "return"
    )

    messages.success(request, "Equipment returned successfully")
    return redirect('borrow_list')


# DELETE BORROW

@login_required
def delete_borrow(request, pk):

    borrow = get_object_or_404(BorrowRequest, pk=pk)

    if borrow.user != request.user:
        return HttpResponseForbidden()

    if borrow.status == 'pending':
        borrow.delete()
        messages.success(request, "Borrow request cancelled")

    return redirect('borrow_list')


# NOTIFICATIONS

@login_required
def notifications(request):

    notifs = request.user.notifications.all().order_by('-created_at')

    return render(request, 'notifications.html', {
        'notifs': notifs
    })