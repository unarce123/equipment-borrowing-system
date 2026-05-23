from django import forms
from .models import BorrowRequest
from equipment.models import Equipment, Category


class BorrowRequestForm(forms.ModelForm):

    # CATEGORY
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border rounded-xl'
        })
    )

    class Meta:
        model = BorrowRequest

        fields = [
            'category',
            'equipment',
            'quantity',
            'borrow_date',
            'return_date',
        ]

        widgets = {

            'equipment': forms.Select(attrs={
                'class': 'w-full p-3 border rounded-xl'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'w-full p-3 border rounded-xl'
            }),

            'borrow_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'w-full p-3 border rounded-xl'
                }
            ),

            'return_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'w-full p-3 border rounded-xl'
                }
            ),
        }

    # FILTER EQUIPMENT BY CATEGORY
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['equipment'].queryset = Equipment.objects.all()

        if 'category' in self.data:

            try:
                category_id = int(self.data.get('category'))

                self.fields['equipment'].queryset = Equipment.objects.filter(
                    category_id=category_id
                )

            except (ValueError, TypeError):
                pass

    # VALIDATE QUANTITY
    def clean_quantity(self):

        quantity = self.cleaned_data.get('quantity')

        equipment = self.cleaned_data.get('equipment')

        if equipment and quantity > equipment.quantity:

            raise forms.ValidationError(
                f"Only {equipment.quantity} equipment available."
            )

        return quantity