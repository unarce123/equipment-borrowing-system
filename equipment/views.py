from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Equipment
from .forms import EquipmentForm
from accounts.utils import is_staff, is_admin


# =========================
# EQUIPMENT LIST (SEARCH + FILTER)
# =========================
@login_required
def equipment_list(request):
    items = Equipment.objects.all()

    # SEARCH
    search = request.GET.get('search')
    if search:
        items = items.filter(name__icontains=search)

    # FILTER BY STATUS
    status = request.GET.get('status')
    if status and status != "all":
        items = items.filter(status=status)

    return render(request, 'equipment/list.html', {
        'items': items,
        'search': search,
        'status': status
    })


# STAFF CAN ADD
@login_required
@user_passes_test(is_staff)
def add_equipment(request):
    form = EquipmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('equipment_list')

    return render(request, 'equipment/form.html', {'form': form})


# STAFF CAN EDIT
@login_required
@user_passes_test(is_staff)
def edit_equipment(request, pk):
    item = get_object_or_404(Equipment, pk=pk)
    form = EquipmentForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('equipment_list')

    return render(request, 'equipment/form.html', {'form': form})


# ADMIN ONLY DELETE
@login_required
@user_passes_test(is_admin)
def delete_equipment(request, pk):
    item = get_object_or_404(Equipment, pk=pk)
    item.delete()
    return redirect('equipment_list')