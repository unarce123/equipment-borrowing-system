from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Equipment
from .forms import EquipmentForm
from accounts.utils import is_staff, is_admin


@login_required
def equipment_list(request):
    query = request.GET.get('q')
    items = Equipment.objects.all()

    if query:
        items = items.filter(name__icontains=query)

    return render(request, 'equipment/list.html', {
        'items': items,
        'query': query
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