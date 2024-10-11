from django import forms
from .models import Wishlist


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.HiddenInput(),
            'quantity': forms.NumberInput(attrs={'min': 1, 'max': 99, 'value': 1})
        }
