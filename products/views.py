from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

def all_products(request):
    '''a view to return all products, including sorting and search queries'''

    products = Product.objects.all() #return all products from database
 
    context = { #make products available in template
        'products': products
    }

    return render(request, 'products/products.html', context) #context needed to add to database later on


def product_detail(request, product_id):
    '''a view to return specific product details'''

    product = get_object_or_404(Product, pk=product_id) #return specifi product based on id
 
    context = { #make products available in template
        'product': product
    }

    return render(request, 'products/product_details.html', context) #context needed to add to database later on