from django.shortcuts import render

# Create your views here.
from django.forms import ValidationError
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.contrib import auth,messages
from django.contrib.auth.models import User
from django.db.models import Q
from accounts.forms import CreateUserForm
# from admin_side.views import *
# from user_side.views import *
from django.shortcuts import get_object_or_404, redirect

from admin_category.models import Category
from admin_products.models import Product
from cart.models import Cart


from .models import *
from django.core.mail import send_mail,EmailMessage
import random

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import PasswordChangeForm



# Create your views here
def users(request):

    

    user=Customer.objects.all().order_by('id')[1:]

    return render(request, 'users.html',{'user':user},)








# def categories(request):

#     return render(request,'categories.html')




def blockuser(request, id):
    # user = get_object_or_404(User, id=id)
    user=Customer.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        messages.success(request, "user has been blocked.")
    else:
        user.is_active = True
        messages.success(request, "user has been unblocked.")
    user.save()
    return redirect(users)



def extraimg(request):
    return render(request,'addextraimg.html')


def profile(request):

    
    return render(request,'profile.html')


    
def about(request):
     return render(request,'about.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['user_name']  # Assuming the email input field is named 'user_name'
        password = request.POST['pass_word']
        
        # Find the user by email
        try:
            user = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            user = None
        
        if user is not None:
            # Authenticate with the user's username and the provided password
            user = auth.authenticate(username=user.username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid password.')
        else:
            messages.error(request, 'No account found with this email.')

    return render(request, 'signin.html')

def logout(request):
    auth.logout(request)
    # if 'username' in request.session:
    #     request.session.flush()
    return redirect('index')

def register(request):
    usr = None
    #Register Form
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        # OTP Verification
        if get_otp:
            get_usr=request.POST.get('usr')
            usr=Customer.objects.get(username=get_usr)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                messages.success(request,f'Account is created for {usr.username}')
                return redirect(login)
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request,'signup.html',{'otp':True,'usr':usr})
        form = CreateUserForm(request.POST)
        #Form Validation
        if form.is_valid():
            form.save()
            email=form.cleaned_data.get('email')
            username=form.cleaned_data.get('username')
            usr=Customer.objects.get(username=username)
            usr.email=email
            usr.username=username
            usr.is_active=False
            usr.save()
            usr_otp=random.randint(100000,999999)
            UserOTP.objects.create(user=usr,otp=usr_otp)
            mess=f'Hello\t{usr.username},\nYour OTP to verify your account for BATMUSIC is {usr_otp}\nThanks!'
            send_mail(
                    "welcome to BATMUSIC-Verify your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [usr.email],
                    fail_silently=False
                )
            messages.info(request,f'OTP send to your email')

            return render(request,'signup.html',{'otp':True,'usr':usr})
            
        else:
            errors = form.errors
            for field, errors in errors.items():
              for error in errors:
                messages.error(request, f" {error}")
                       
    #Resend OTP
    elif (request.method == "GET" and 'username' in request.GET):
        get_usr = request.GET['username']
        if (Customer.objects.filter(username = get_usr).exists() and not Customer.objects.get(username = get_usr).is_active):
            usr = Customer.objects.get(username=get_usr)
            id = usr.id
            
            otp_usr = UserOTP.objects.get(user_id=id)
            usr_otp=otp_usr.otp
            mess = f"Hello, {usr.username},\nYour OTP is {usr_otp}\nThanks!"
            
            send_mail(
        "Welcome to BATMUSIC - Verify Your Email",
        mess,
        settings.EMAIL_HOST_USER,
        [usr.email],
        messages.success(request, f'OTP resend to  {usr.email}'),

        # fail_silently = False
         )
        return render(request,'signup.html',{'otp':True,'usr':usr})
    else:
            errors = ''
    form=CreateUserForm()
    context = {'form': form, 'errors': errors}

    return render (request, 'signup.html', context)













def password_reset(request):

    return render (request,'password_reset.html')



def remove_coupon(request):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart.coupon = None
        cart.save()
        messages.success(request, 'Coupon removed successfully')
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))






@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            update_session_auth_hash(request, user)
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepass.html', {'form': form})


def login_required_decorator(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

change_password = login_required_decorator(change_password)


def resetpassword_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Customer._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError,Customer.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']=uid
        messages.success(request,"  Please reset your password")
        return redirect('resetpassword')
    else:
        messages.error(request,"This link has been expired")
        return redirect('login')
    

def forgetpassword(request):
    if request.method=="POST":
        email=request.POST['email']
        if Customer.objects.filter(email=email).exists():
            user=Customer.objects.get(email__exact=email)
           #reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_site,
             
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                 # Generate a token for a user also
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email=EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            send_email.send()

            messages.success(request,"Password reset email has been sent to your email")
            
            return redirect('login')
        else:
            messages.error(request,'Account does not exists')
            return redirect('login')
    return render(request,'forgetpassword.html')


def resetpassword(request):
   if request.method=="POST":
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password == confirm_password:
            uid=request.session.get('uid')
            user= Customer.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,"Password reset successful")
            return redirect('login')
        else:
          messages.error(request,"Password not match")
          return redirect('resetPassword')
   else:
     return render (request,'resetPassword.html')






def coupons(request):

    return render(request, 'coupouns.html')