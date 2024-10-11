from sre_parse import CATEGORIES
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Customer


from .models import Category
from django.utils.text import slugify
from django.contrib import auth,messages
from django.db.models import Q 




# Create your views here.

def addcategory(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        cat_image = request.FILES.get('cat_image')

        # slug = slugify(name)

        category = Category(category_name=name, description=description, cat_image= cat_image)
        category.save()

        msg = "Category added"
        return redirect('categories')

    return render(request, 'cat.html', locals())


def categories(request):
      
    context=Category.objects.all().order_by('id')


    return render(request,'cm.html',{'cat':context})


def delcategories(request,categories_id):

    dele=Category.objects.get(id=categories_id)
    dele.delete()


    return redirect(categories)




def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        cat_image = request.FILES.get('cat_image')
        
        if name and description:
            category.category_name = name
            category.description = description
            
            if cat_image:
                category.cat_image = cat_image
                
            category.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('categories')
        
        else:
            messages.error(request, 'Please provide a category name and description.')
    
    context = {
        'category': category
    }
    
    return render(request, 'edit_category.html', context)




# def CatSearch(request):
    
#     categories = Category.objects.none()  # Initialize products with an empty queryset
#     categories_count = 0  # Initialize products_count with 0
    
#     if 'keyword' in request.GET:
#         keyword = request.GET['keyword']
        
#         print(keyword)
#         if keyword:
#             categories = Category.objects.filter(Q(description=keyword) | Q(category_name__icontains=keyword) )
#             categories_count = categories.count()

#     context = {
#         'use': categories,
#         'categories_count': categories_count,
#     }

#     return render(request, 'cm.html', context)




def CatSearch(request):
    print(request.GET)
    cat = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            cat = Category.objects.filter(category_name__icontains=keyword)
            
            if not cat:
                message = "No products found for the keyword entered."
                context = {
                    'message': message
                }
                return render(request, 'cm.html', context)
                
    context = {}
    if cat is not None:
        context['cat'] = cat
        
    return render(request, 'cm.html', context)
  