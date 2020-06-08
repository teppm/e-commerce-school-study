from django.shortcuts import render, get_object_or_404, redirect, reverse 
from django.contrib import messages
from .models import Product
from django.db.models import Q #special object used to generate a search query ##find info in the queries portion of django docs

# Create your views here.

def all_products(request):
    '''a view to return all products, including sorting and search queries'''

    products = Product.objects.all() #return all products from database
    query = None #start with empty query so we dont get error on products page without a search term

    if request.GET: #if we receive a request.get from form
        if 'q' in request.GET:  #if in the request.get we have q(name for the search field in form)
            query = request.GET['q'] #we generate variable with that content
            if not query: #if no query variable created
                messages.error(request, 'You did not enter any search criteria!') #return messages
                return redirect(reverse('product')) #and redirect to product page

            queries = Q(name__icontains=query) | Q(description__icontains=query) #creating or logic if query variable is found in either name or description return it
            products = products.filter(queries) #adding queries to the filter

            
 
    context = { #make products available in template
        'products': products,
        'search_term': query #search term is either the empty query or the request.get generated one
    }

    return render(request, 'products/products.html', context) #context needed to add to database later on


def product_detail(request, product_id):
    '''a view to return specific product details'''

    product = get_object_or_404(Product, pk=product_id) #return specifi product based on id
 
    context = { #make products available in template
        'product': product
    }

    return render(request, 'products/product_details.html', context) #context needed to add to database later on