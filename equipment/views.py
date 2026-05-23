from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator

from .models import Equipment, Category
from .forms import EquipmentForm

from accounts.utils import is_staff, is_admin



# SAFE CLEAN FUNCTION

def clean(value):
    if value in [None, "", "None", "all"]:
        return None
    return value



# EQUIPMENT LIST

@login_required
def equipment_list(request):

    items = Equipment.objects.all()
    categories = Category.objects.all()

    # CLEAN INPUTS
    search = clean(request.GET.get('search'))
    category = clean(request.GET.get('category'))
    status = clean(request.GET.get('status'))

    # SEARCH
    if search:
        items = items.filter(name__icontains=search)

    # CATEGORY FILTER
    if category:
        items = items.filter(category_id=category)

    # STATUS FILTER
    if status:
        items = items.filter(status=status)

    # PAGINATION
    paginator = Paginator(items.order_by('-id'), 10)
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)

    return render(request, 'equipment/list.html', {
        'items': items,
        'categories': categories,
        'search': search or "",
        'category': category or "all",
        'status': status or "all",
    })


# =========================
# ADD EQUIPMENT
# =========================
@login_required
@user_passes_test(is_staff)
def add_equipment(request):

    form = EquipmentForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('equipment_list')

    return render(request, 'equipment/form.html', {
        'form': form
    })


# =========================
# EDIT EQUIPMENT
# =========================
@login_required
@user_passes_test(is_staff)
def edit_equipment(request, pk):

    item = get_object_or_404(Equipment, pk=pk)

    form = EquipmentForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('equipment_list')

    return render(request, 'equipment/form.html', {
        'form': form
    })


# =========================
# DELETE EQUIPMENT
# =========================
@login_required
@user_passes_test(is_admin)
def delete_equipment(request, pk):

    item = get_object_or_404(Equipment, pk=pk)
    item.delete()

    return redirect('equipment_list')