from django.urls import path, include
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views






urlpatterns = [

    path('addcategory/',views.addcategory,name='addcategory'),
    path('delcategories/<int:categories_id>/',views.delcategories ,name='delcategories'),
    path('categories/',views.categories,name='categories'),
    path('edit_category/<int:category_id>',views.edit_category,name='edit_category'),
    path('CatSearch/',views.CatSearch,name='CatSearch'),
]