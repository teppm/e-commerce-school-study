from django.shortcuts import render
from .models import Product

# Create your views here.

def all_products(request):
    '''a view to return all products, including sorting and search queries'''

    products = Product.objects.all() #return all products from database
 
    context = { #make products available in template
        'products': products
    }

    return render(request, 'products/products.html', context) #context needed to add to database later on