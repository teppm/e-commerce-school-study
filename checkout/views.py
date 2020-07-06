from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from bag.contexts import bag_contents
from django.conf import settings
import stripe

# Create your views here.

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY 
    stripe_secret_key = settings.STRIPE_SECRET_KEY 

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