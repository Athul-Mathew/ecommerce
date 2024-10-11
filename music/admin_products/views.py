from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q 
from admin_brand.models import Brand
from admin_products.models import Product, ProductImage, ProductOffer
from admin_category.models import Category
# Create your views here.
from django.contrib import auth,messages

def product(request):
    products = Product.objects.all()
    product_offers = ProductOffer.objects.all()

    context = {'products': products, 'product_offers': product_offers}

    return render(request, 'products.html', context)


def addproducts(request):
    category = Category.objects.all()
    brand = Brand.objects.all()

    

    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        
        cat = request.POST['category']
        stock  =request.POST['stock']
        desc = request.POST['desc']
        image_1 = request.FILES['image1']
      

        brand1=request.POST['brand']
        

        # slug = slugify(name)

        catobj = Category.objects.get(id=cat)
        brand_instance = Brand.objects.get(id=brand1)
        Product.objects.create( product_name=name, price=price,  category=catobj, stock=stock, description=desc, images1=image_1,brand=brand_instance)
        # messages.success(request, "Product added")
        return redirect(addproducts)
        
   
    context ={
        'brands': brand,
        'category':category,
    }
    # return render(request,'addproduct.html',locals())
    return render(request,'addproduct.html',context)



def updateproduct(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        name = request.POST['name']
        print("==========================")
        print(name)

        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        
        if name:
            product.product_name = name
        
        if request.POST['image']:
            image = request.FILES['image']
            product.images1 = image
        
        if description:
            product.description = description
        
        if price:
            product.price = price

        if  stock:
            product.stock = stock

        
        product.save()
        return redirect('product')
    
    return render(request, 'edit-product.html', {'product': product})


def add_product_images(request, product_id):
    # Get the product object
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Get the list of uploaded images from the request
        images = request.FILES.getlist('images')

        # Create a new product image object for each uploaded image
        for image in images:
            product_image = ProductImage(product=product, image=image)
            product_image.save()

        messages.success(request, 'Images added successfully.')
        return redirect('product')

    return render(request, 'addextraimg.html', {'product': product})


  



def deleteproduct(request,product_id):

    dele=Product.objects.get(id=product_id)
    dele.delete()


    return redirect(product)





def add_product_offer(request, product_id):
    # Get the product object
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Get the offer details from the form
        offer_price = request.POST.get('offer_price')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Create a new product offer object
        product_offer = ProductOffer(product=product, offer_price=offer_price, start_date=start_date, end_date=end_date)
        product_offer.save()

        messages.success(request, 'Product offer added successfully.')
        return redirect('product')

    return render(request, 'addoffer.html', {'product1': product})

def delete_product_offer(request, offer_id):
    # Get the product offer object
    product_offer = get_object_or_404(ProductOffer, id=offer_id)

    # Delete the product offer
    product_offer.delete()

    messages.success(request, 'Product offer deleted successfully.')
    return redirect('product')
