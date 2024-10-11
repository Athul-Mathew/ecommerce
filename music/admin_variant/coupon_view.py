from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Product_Variant
from .models import Coupon
from django.shortcuts import render, redirect, get_object_or_404
from .models import Coupon
from .forms import CouponForm


def coupon_list(request):
    coupons = Coupon.objects.all()
    context = {'coupons': coupons}
    return render(request, 'coupon_list.html', context)


def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupon_list')
    else:
        form = CouponForm()
    context = {'form': form}
    return render(request, 'coupon_form.html', context)


def edit_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('coupon_list')
    else:
        form = CouponForm(instance=coupon)
    context = {'form': form}
    return render(request, 'coupon_form.html', context)


def delete_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        coupon.delete()
        return redirect('coupon_list')
    context = {'coupon': coupon}
    return render(request, 'coupon_confirm_delete.html', context)
