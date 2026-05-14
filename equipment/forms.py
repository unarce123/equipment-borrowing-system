from django import forms
from .models import Equipment


INPUT_CLASS = (
    'w-full border border-gray-300 rounded-xl p-3 '
    'focus:ring-2 focus:ring-blue-500 focus:outline-none'
)


class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment
        fields = ['name', 'category', 'quantity', 'status', 'description']

        widgets = {

            'name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Enter equipment name'
            }),

            'category': forms.Select(attrs={
                'class': INPUT_CLASS,
            }),

            'quantity': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Enter quantity'
            }),

            'status': forms.Select(attrs={
                'class': INPUT_CLASS,
            }),

            'description': forms.Textarea(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Enter description',
                'rows': 4
            }),
        }