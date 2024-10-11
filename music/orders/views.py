import os
from django.shortcuts import render
import razorpay
from checkout.models import OrderItem, Order
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from razorpay.errors import BadRequestError,ServerError

def view(request):

    return render(request,'invoice.html')

def order_items(request,id):
    order = Order.objects.get(user=request.user, id=id)
    ordered_items = OrderItem.objects.filter(order=order).order_by('-id')
    context = {
        'orders' : order,
        'ordered_items' : ordered_items
    }

    return render(request,'orderitems.html',context)


def cancelOrder(request):
    if request.method == 'POST':
            id = request.POST.get('id')

    client = razorpay.Client(auth=(os.getenv("KEY_ID"), os.getenv("SECRET_KEY")))
    try:
        order = Order.objects.get(id=id,user=request.user)
    except Order.DoesNotExist:
        # Handle the case where the order does not exist
        order = None
    
    if order is None:
        # Render an error message if the order does not exist
        messages.warning(request,'The order you are trying to cancel does not exist.')
        return redirect(order)
    
    payment=order.payment
    msg=''
    
    if (payment.payment_method == 'Paid by Razorpay'):
        payment_id = payment.payment_id
        amount = payment.amount_paid
        amount= amount*100
        try :
            # captured_amount = client.payment.capture(payment_id,amount)
            pass
        except BadRequestError as e:
            # Handle a BadRequestError from Razorpay
            captured_amount = None
            messages.warning(request,'The payment has not been captured.Please try again later. If the issue continues, CONTACT THE SUPPORT TEAM!')
            return redirect(order)
        #   except ServerError as e:
              # Handle a ServerError from Razorpay
        #   captured_amount = None
            # msg = "Server error occurred while capturing the payment."

        # if captured_amount is not None and captured_amount['status'] == 'captured' :
        #     refund_data = {
        #         "payment_id": payment_id,
        #         "amount": amount,  # amount to be refunded in paise
        #         "currency": "INR",
        #     }
            
        #     refund = client.payment.refund(payment_id, refund_data)
            #  except BadRequestError as e:
            #      # Handle a BadRequestError from Razorpay
            #      refund = None
            #      msg = "Bad request error occurred while processing the refund."
            #  except ServerError as e:
            #      # Handle a ServerError from Razorpay
            #      refund = None
            #      msg = "Server error occurred while processing the refund."
            # print(refund)
            
            if refund is not None:
                current_user=request.user
                order.refund_completed = True
                order.status = 'Cancelled'
                payment = order.payment
                payment.refund_id = refund['id']
                payment.save()
                order.save()
                messages.success(request,'Your order has been successfully cancelled and amount has been refunded!')
                mess=f'Hai\t{current_user.username},\nYour order has been canceled, Money will be refunded with in 1 hour\nThanks!'
                try:
                    send_mail(
                            "Order Cancelled",
                            mess,
                            settings.EMAIL_HOST_USER,
                            [current_user.email],
                            fail_silently = False
                        )
                except Exception as e:
                    # Handle an exception while sending email
                    msg += "\nError occurred while sending an email notification."
            else :
                messages.warning(request,'Your order is not cancelled because the refund could not be completed now. Please try again later. If the issue continues, CONTACT THE SUPPORT TEAM!')
                pass
        else :
            if(payment.paid):
                order.refund_completed = True
                order.status = 'Cancelled'
                messages.success(request,'YOUR ORDER HAS BEEN SUCCESSFULLY CANCELLED!')
                order.save()
            else:
                order.status = 'Cancelled'
                order.save()
                messages.success(request,'Your payment has not been recieved yet. But the order has been cancelled.!')
    else :
        order.status = 'Cancelled'
        messages.success(request,'YOUR ORDER HAS BEEN SUCCESSFULLY CANCELLED!')
        order.save()
    return redirect('order')




def order_list(request):
    orders = OrderItem.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

    

def change_order_status(request, order_id):
    order = get_object_or_404(OrderItem, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        order.order_status = new_status
        order.save()
        return redirect('order_list')
    return render(request, 'change_order_status.html', {'order': order})


def admin_sales(request):
    context = {}

    if request.method == 'POST':

        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')

        if start_date == '' or end_date == '':
            messages.error(request,'Give date first')
            return redirect(admin_sales)

        order_items = OrderItem.objects.filter(order__ordered_date__gte=start_date, order__ordered_date__lte=end_date).order_by('-id')

        if order_items:
            context.update(sales = order_items,s_date=start_date,e_date = end_date)
        else:
            messages.error(request,'no data found')

    return render(request,'admin_sales.html',context)    
