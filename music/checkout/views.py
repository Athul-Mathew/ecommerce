import datetime
from http.client import PAYMENT_REQUIRED
import random

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render,HttpResponse
from django.contrib import messages
from accounts.models import Customer
from admin_products.models import Product
import razorpay
from .models import OrderItem, Payment, Order
from django.core.mail import send_mail
from django.utils import timezone
from cart.models import *
import orders
from user_profile.models import AddressDetails# Create your views here.










def checkout(request):
    # get the current user
    current_user = request.user
    
    # get the user's saved addresses
    addresses = AddressDetails.objects.filter(user=current_user).order_by('id')
    
    # get the user's active cart
    try:
        cart = Cart.objects.get(user=current_user, is_active=True)
    except Cart.DoesNotExist:
        # redirect the user to their cart if they don't have an active cart
        return redirect('show_cart')
    
    # get the cart items and check if any have an invalid quantity
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        if item.quantity > item.product.stock:
            item.quantity = item.product.stock
            item.save()
            messages.warning(request, f'{item} has only {item.product.stock} quantity left')
            return redirect('show_cart')
    
    # create a Razorpay order for the cart total amount
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    amount = int(cart.get_cart_total() * 100) # convert to paise
    currency = 'INR'
    payment = client.order.create({'amount': amount, 'currency': currency, 'payment_capture': 1})
    print(payment)
    # save the Razorpay order ID to the cart
    cart.razorpay_order_id = payment['id']
    cart.save()


    
    # define the context data to pass to the template
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'addresses': addresses,
        'payment': payment,
    }
    
    # render the checkout page template with the context data
    return render(request, 'checkout.html', context)




def success(request):
    # try:
        print('success function is called')
        print(request.GET)
        razorpay_order_id = request.GET.get('razorpay_order_id')
        print("===========================================")
        print(razorpay_order_id)
        print('not this')
        cart = Cart.objects.get(razorpay_order_id=razorpay_order_id)
        print('cart obj error')

        # Payment details storing
        user = request.user
        transaction_id = request.GET.get('razorpay_payment_id')
        print('getiing cart total')
        cart_total = cart.get_cart_total()
        print('getting cart tax')
        # tax = cart.get_tax()
        
        
        print('gettingf g totalla')

        payment = Payment.objects.create(user=user, transaction_id=transaction_id, cart_total=cart_total)
        payment.save()
        
        print('before adderess')
        address_id = request.GET.get('address')
        print('address  : ' , address_id)
        delivery_address = AddressDetails.objects.get(user=user, id=address_id)
        
        # Creating the order in Order table
        order = Order.objects.create(order_id=razorpay_order_id, user=user, delivery_address=delivery_address, payment=payment)

        if cart.coupon:
            order.coupon = cart.coupon
            order.save()

        # Storing ordered products in OrderItem table
        order_items = CartItem.objects.filter(cart=cart)
        for item in order_items:
            item.product.stock -= item.quantity
        
            item.product.save()
        
            ordered_item = OrderItem.objects.create(user=user,order=order, product=item.product, item_price=item.get_product_price(), quantity=item.quantity, item_total=item.get_item_total())
        

            ordered_item.save()
            
       

        # Deleting the cart once it is ordered/paid
        cart.is_active = False
        cart.delete()

        return render(request, 'success.html', {'order_id': razorpay_order_id})
    
    # except:
    #     return redirect('orders_list')


def orders_list(request):
    orders = Order.objects.filter(user=request.user)
    # order_items = OrderItem.objects.filter(order=orders)
    return render(request, 'orderlist.html', {'orders' : orders})


def order_details(request,order_id):
    try:
        order = Order.objects.get(uid=order_id)
        order_items = OrderItem.objects.filter(order=order)
        print(order_items)
    except:
        order_items = None
        
    return render(request, 'orders/order_details.html', {'order_items' : order_items})


def order_tracking(request, item_id):
    current_date = timezone.now()
    item = OrderItem.objects.get(id=item_id)

    context = {
        'item' : item,
        'current_date' : current_date
    }
    return render(request, 'orders/order_tracking.html' ,context)



def order_invoice(request, order_id):

    order = Order.objects.get(uid=order_id,user=request.user)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order' : order,
        'order_items' : order_items
    }
    return render(request, 'orders/invoice.html',context)


def cancel_order(request, item_id=None, order_id=None):
        
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        order = Order.objects.get(order_id=order_id,user=request.user)
        payment_id = order.payment.transaction_id
        item = OrderItem.objects.get(order=order, id=item_id)
        item_amount = int(item.item_total) * 100
        
        refund = client.payment.refund(payment_id,{'amount':item_amount})

        if refund is not None:
            item.order_status = 'Refunded'
            item.product.stock += item.quantity
            item.product.save()

            current_user = request.user
            subject = "Refund succesfull!"
            mess = f'Greetings {current_user.first_name}.\nYour refund for the product {item} of order: {order.order_id} has been succesfully generated. \nThank you for shopping with us!'
            send_mail(
                        subject,
                        mess,
                        settings.EMAIL_HOST_USER,
                        [current_user.email],
                        fail_silently = False
                     )

            item.save()
            return render(request, 'orders/refund_success.html',{'order_id':order_id})

        else:
            return HttpResponse('Payment not captured')
    