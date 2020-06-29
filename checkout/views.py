from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm

# Create your views here.

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'Theres nothing in your bag at this moment')
        return redirect(reverse, ('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51GzOgPI48rFGEYTAv9VjTLFRSOPaWqQ9kxtmwtUUSQxhso9IY5ivNZ28yUqdXti1ssf6DjT3OgNnpkcZ3NNeKayS00r0mY2nUi',
        'client_secret': 'test client secret'
    }

    return render(request, template, context)