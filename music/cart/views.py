from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render



from admin_products.models import Product
from admin_variant.models import Coupon
from cart.models import Cart, CartItem


# Create your views here.

def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        user = request.user

        cart, _ = Cart.objects.get_or_create(user=user, is_active=True)
        is_cart_item = CartItem.objects.filter(cart=cart, product=product).exists()

        if is_cart_item:
            cart_item = CartItem.objects.get(cart=cart, product=product)

            if cart_item.quantity == product.stock:
                messages.error(request, f'Only {cart_item.quantity} product in stock')
                return redirect('cart')

            cart_item.quantity += 1
            cart_item.save()

        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            cart_item.save()

    except Product.DoesNotExist:
        messages.error(request, "Product does not exist.")
        return redirect('cart')

    return redirect('show_cart')






# 
def show_cart(request):
    cart=None
    cart_items=None
    
    try:
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
        cart_items = CartItem.objects.filter(cart=cart).order_by('id')
        coupons = Coupon.objects.filter(is_expired=False)
        print(coupons)
    except Exception as e:
        print(e)

    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(name__icontains=coupon)



        if not coupon_obj.exists():
            messages.error(request, 'Invalid Coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart.coupon:
            messages.warning(request, 'Coupon Already applied')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart.get_cart_total() < coupon_obj[0].min_amount:
            messages.warning(
                request, f'Total amount should be greater than ₹{coupon_obj[0].min_amount} excluding tax')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj[0].is_expired:
            messages.warning(request, 'This coupon has expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
       
        cart.coupon = coupon_obj[0]
        cart.save()
        messages.success(request, 'Coupon Applied')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {'cart_items': cart_items,
               'cart': cart,
               'coupons' : coupons,
               

               }
    return render(request, 'shopping-cart.html', context)



# def remove_from_cart(request,cart_id, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     try:
#         cart_item = Cart.objects.get(id=cart_id)
#     except Cart.DoesNotExist:
#         messages.warning(request, "This product is not in your cart")
#         return redirect('show_cart')
#     cart_item.delete()
#     messages.success(request, f"{product.product_name} has been removed from your cart.")
#     return redirect('show_cart')


def remove_from_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        user = request.user

        cart = Cart.objects.get(user=user, is_active=True)
        cart_item = CartItem.objects.get(cart=cart, product=product)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete()

        messages.success(request, "Product removed from cart successfully")

    except (Product.DoesNotExist, Cart.DoesNotExist, CartItem.DoesNotExist):
        messages.error(request, "An error occurred while removing the product from cart")

    return redirect('show_cart')




def remove_coupon(request):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart.coupon = None
        cart.save()
        messages.success(request, 'Coupon removed successfully')
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cartitem(request, product):
    try:
        product = Product.objects.get(id=product)
        cartt = Cart.objects.get(user=request.user, is_active=True)
        cart_item = CartItem.objects.get(cart=cartt, product=product)

        cart_item.delete()
        messages.success(request, "Product deleted from cart successfully")

    except:
        pass

    return redirect(show_cart)