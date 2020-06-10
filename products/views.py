from django.shortcuts import render, get_object_or_404, redirect, reverse 
from django.contrib import messages
from .models import Product, Category
from django.db.models import Q #special object used to generate a search query ##find info in the queries portion of django docs

# Create your views here.

def all_products(request):
    '''a view to return all products, including sorting and search queries'''

    products = Product.objects.all() #return all products from database
    query = None #start with empty query so we dont get error on products page without a search term
    categories = None #starting with empty for same reason as above
    sort = None #starting with empty for same reason as above
    direction = None #starting with empty for same reason as above

    if request.GET: #if we receive a request.get from form
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if 'sortkey' == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if 'sortkey' == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET: #checking if category exists in request.get
            categories = request.GET['category'].split(',') # create variable with request.get content and split list from comma
            products = products.filter(category__name__in=categories) #And then use that list to filter the current query set of all products down to only products whose category name is in the list.
            categories = Category.objects.filter(name__in=categories) # we  convert list of strings into a list of actual category objects, so that we can access all their fields in the template.


        if 'q' in request.GET:  #if in the request.get we have q(name for the search field in form)
            query = request.GET['q'] #we generate variable with that content
            if not query: #if no query variable created
                messages.error(request, 'You did not enter any search criteria!') #return messages
                return redirect(reverse('product')) #and redirect to product page

            queries = Q(name__icontains=query) | Q(description__icontains=query) #creating or logic if query variable is found in either name or description return it
            products = products.filter(queries) #adding queries to the filter

    
    current_sorting = f'{sort}_{direction}'
 
    context = { #make products available in template
        'products': products,
        'search_term': query, #search term is either the empty query or the request.get generated one
        'current_categories': categories,
        'current_sorting' : current_sorting
    }

    return render(request, 'products/products.html', context) #context needed to add to database later on


def product_detail(request, product_id):
    '''a view to return specific product details'''

    product = get_object_or_404(Product, pk=product_id) #return specifi product based on id
 
    context = { #make products available in template
        'product': product
    }

    return render(request, 'products/product_details.html', context) #context needed to add to database later on