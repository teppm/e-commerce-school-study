from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """Instead of returning a template though this function will return a dictionary
called context which were about to create.
This is what's known as a context processor.
And its purpose is to make this dictionary available to all templates across the entire application"""

    bag_items = []
    total = 0
    product_count = 0 
    bag = request.session.get('bag', {}) # Accessing the shopping bag in the session is simple , Getting it if it already exists. Or initializing it to an empty dictionary if not.

    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id':item_id,
                'quantity': item_data,
                'product': product     
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size
                })


    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else: 
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items':bag_items,
        'total':total,
        'product_count':product_count,
        'delivery':delivery,
        'free_delivery_delta':free_delivery_delta,
        'free_delivery_threshold':settings.FREE_DELIVERY_THRESHOLD,
        'grand_total':grand_total
    }

    return context