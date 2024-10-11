from django.shortcuts import render
from ad_banner.models import banner
from admin_products.models import Product

# Create your views here.
def index(request):
    try:
        context= Product.objects.all()[:8]
        banners = banner.objects.all()

    except:
        context = None

    return render(request, 'index.html',{'use':context,'baner':banners})