from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import OrderForm
from products.models import Product
from .models import Order, OrderLineItem
from bag.contexts import bag_contents
from django.conf import settings
import stripe

# Create your views here.

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY 
    stripe_secret_key = settings.STRIPE_SECRET_KEY 
    
    if request.method == 'POST':

        bag = request.session.get('bag', {})

        form_data = {
            'full_name' : request.POST['full_name'],
            'email' : request.POST['email'],
            'phone_number' : request.POST['phone_number'],
            'country' : request.POST['country'],
            'postcode' : request.POST['postcode'],
            'town_or_city' : request.POST['town_or_city'],
            'street_address1' : request.POST['street_address1'],
            'street_address2' : request.POST['street_address2'],
            'county' : request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size
                            )
                            order_line_item.save()

                except Product.DoesNotExist:
                    messages.error(request, (
                        "One or more of the products in your bag was not found in our database."
                        "Please call for assistance!")
                    )
                    order.delete()
                    return redirect(reverse, ('view_bag'))
            
            request.session['save_info'] = 'save_info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))            
        else: 
            messages.error(request, 'There was an error!')

    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, 'Theres nothing in your bag at this moment')
            return redirect(reverse, ('products'))

        current_bag =  bag_contents(request) #get bag_content def from bag.contexts
        total = current_bag['grand_total'] #access grand_total key from bag_content
        stripe_total = round(total * 100) #multiply that by a hundred and round it to zero decimal places using the round function.Since stripe will require the amount to charge as an integer.
        stripe.api_key = stripe_secret_key #set the secret key on stripe.
        intent = stripe.PaymentIntent.create( #create the payment intent with stripe.payment.intent.create giving it the amount and the currency.
            amount = stripe_total,
            currency = settings.STRIPE_CURRENCY
        )

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
                         Did you forget to set it in your environment?')

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkout!
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order succesfully processed!\
                    You will be sent a confirmation e-mail within short to {order.email}!\
                    Your order number is: {order_number}')
    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'   
    context = {
        'order': order
    } 

    return render(request, template, context)