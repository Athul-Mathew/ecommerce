from django import forms
from .models import Coupon


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['name', 'min_amount', 'discount_price', 'is_expired']
