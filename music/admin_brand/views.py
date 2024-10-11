from django.shortcuts import redirect, render

from admin_brand.models import Brand

# Create your views here.
def brand(request):

    context=Brand.objects.all()


    return render(request,'brands.html',{'brands':context})
        
def addbrand(request):
    if request.method == 'POST':
        name = request.POST['brand_name']
        description = request.POST['brand_description']
        logo = request.FILES.get('brand_img')
        print("============================================================")
        brand = Brand(brand_name=name, brand_description=description, brand_img=logo)
        brand.save()
        return redirect('brand')
    else:
        return render(request, 'addbrand.html') 
    
from django.shortcuts import render, get_object_or_404, redirect
from .models import Brand

def update_brand(request, brand_id):
    brand = get_object_or_404(Brand, brand_id=brand_id)

    if request.method == 'POST':
        brand.brand_name = request.POST['name']
        brand.brand_description = request.POST['description']

        if request.FILES.get('image'):
            brand.brand_img = request.FILES['image']

        brand.save()

        return redirect('brand')

    context = {
        'brand': brand,
    }

    return render(request, 'editbrand.html', context)



def deletebrand(request,brand_id):

    dele=Brand.objects.get(id=brand_id)
    dele.delete()


    return redirect('brand')    