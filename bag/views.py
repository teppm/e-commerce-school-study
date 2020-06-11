from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """create shopping bag view"""
    return render(request, 'bag/bag.html') 

def add_to_bag(request, item_id):
    """view to add items to bag"""

    quantity = int(request.POST.get('quantity')) #get quantity from form input and change it integer
    redirect_url = request.POST.get('redirect_url') #get redirect url from form input 
    bag = request.session.get('bag', {}) # To implement this concept I'm going to create a variable bag.Which accesses the requests session.Trying to get this variable if it already exists.

    if item_id in list(bag.keys()): # if there's already a key in the bag dictionary matching this product id.
        bag[item_id] += quantity # if there's already a key in the bag dictionary matching this product id. Then I'll increment its quantity accordingly.
    else:
        bag[item_id] = quantity #create a key of the items id and set it equal to the quantity.

    request.session['bag'] = bag #Now I just need to put the bag variable into the session. Which itself is just a python dictionary."
    print(request.session['bag'])
    return redirect(redirect_url)