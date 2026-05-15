from django import forms
from .models import BorrowRequest


class BorrowRequestForm(forms.ModelForm):

    class Meta:
        model = BorrowRequest

        fields = [
            'equipment',
            'quantity',
            'borrow_date',
            'return_date',
        ]

        widgets = {
            'borrow_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'return_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

    # ✅ VALIDATE QUANTITY
    def clean_quantity(self):

        quantity = self.cleaned_data.get('quantity')

        equipment = self.cleaned_data.get('equipment')

        if equipment and quantity > equipment.quantity:

            raise forms.ValidationError(
                f"Only {equipment.quantity} equipment available."
            )

        return quantity