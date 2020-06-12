from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """create shopping bag view"""
    return render(request, 'bag/bag.html') 

def add_to_bag(request, item_id):
    """view to add items to bag"""

    quantity = int(request.POST.get('quantity')) #get quantity from form input and change it integer
    redirect_url = request.POST.get('redirect_url') #get redirect url from form input 
    size = None  #Let's set size equal to none initially
    if 'product_size' in request.POST: # And then if product size is in request.post we'll set it equal to that.
        size = request.POST['product_size']
    bag = request.session.get('bag', {}) # To implement this concept I'm going to create a variable bag.Which accesses the requests session.Trying to get this variable if it already exists.
   
    if size: 
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys(): # If the item is already in the bag. Then we need to check if another item of the same id and same size already exists. And if so increment the quantity for that size and otherwise just set it equal to the quantity.
                bag[item_id]['items_by_size'][size] += quantity # And if so increment the quantity for that size
            else:
                bag[item_id]['items_by_size'][size] = quantity #and otherwise just set it equal to the quantity.
        else:
            bag[item_id] = {'items_by_size': {size: quantity}} # If the items not already in the bag we just need to add it. But we're actually going to do it as a dictionary with a key of items_by_size.
    else:
        if item_id in list(bag.keys()): # if there's already a key in the bag dictionary matching this product id.
            bag[item_id] += quantity # if there's already a key in the bag dictionary matching this product id. Then I'll increment its quantity accordingly.
        else:
            bag[item_id] = quantity #create a key of the items id and set it equal to the quantity.

    request.session['bag'] = bag #Now I just need to put the bag variable into the session. Which itself is just a python dictionary."
    print(request.session['bag']) #print sessions to console to verify that add bag function works, should be removed for production
    return redirect(redirect_url)