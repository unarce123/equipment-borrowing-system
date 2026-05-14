from django import forms
from .models import BorrowRequest


INPUT_CLASS = (
    'w-full border border-gray-300 rounded-xl p-3 '
    'focus:ring-2 focus:ring-blue-500 focus:outline-none'
)


class BorrowRequestForm(forms.ModelForm):

    class Meta:
        model = BorrowRequest
        fields = ['equipment', 'quantity']

        widgets = {

            'equipment': forms.Select(attrs={
                'class': INPUT_CLASS,
            }),

            'quantity': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Enter quantity'
            }),
        }