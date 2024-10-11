from datetime import date
from django.shortcuts import render, HttpResponse
from admin_category.models import Category
from admin_products.models import Product, ProductImage, ProductOffer
from accounts.models import MultiProduct
from admin_brand.models import Brand
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q

# Create your views here.
def shop(request):
    
    if request.GET.get('cat'):
        cat_id = int(request.GET.get('cat'))
        category = Category.objects.get(id=cat_id)
        products = Product.objects.filter(category=category)
       
    elif request.GET.get('brand'):
        br_id = int(request.GET.get('brand'))
        brand = Brand.objects.get(id=br_id)
        products = Product.objects.filter(brand=brand)
    
    elif 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword) )
            products_count = products.count()
        
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    cate=Category.objects.all()
    brands=Brand.objects.all()
    
    return render(request, 'shop.html',{'cat':cate,'use':paged_products,'brands':brands})


def shopdetails(request, id):
    product = Product.objects.get(id=id)
    multipleimg = ProductImage.objects.filter(product=product)
    cate=product.category
    
    try:
        product_offers = ProductOffer.objects.get(product=product)
    except:
        product_offers = None


    context = {
        'pro': product,
        'multipleimg': multipleimg,
        'product_offers': product_offers,
        'category':cate
    }

    return render(request, 'shop-details.html', context)
