from django.http import HttpResponse
from .models import Order, OrderLineItem
from products.models import Product

import json
import time

class StripeWH_Handler:
    """Handle stripe webhooks"""
    """
     we're going to use it to assign the request as an attribute of the class
    just in case we need to access any attributes of the request coming from stripe.    """

    def __init__(self, request):
        self.request = request


    def handle_event(self, event):
        """
        handle generic / unknown / unexpected webhook event
        create a class method called handle event which will take the event stripe is sending us
        and simply return an HTTP response indicating it was received.
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)
        """
        The idea here is that for each type of webhook.
        We want a different method to handle it which makes them easy to manage.
        And makes it easy to add more as stripe adds new ones.
        """

    
    def handle_payment_intent_succeeded(self, event):
        """
        handle payment.intent.succeeded webhooks from stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
        
        """
        The first thing then is to check if the order exists already.
        If it does we'll just return a response, and say everything is all set.
        And if it doesn't we'll create it here in the webhook.
        Let's start by assuming the order doesn't exist.
        We can do that with a simple variable set to false.
        Then we'll try to get the order using all the information from the payment intent.
        And I'm using the iexact lookup field to make it an exact match but case-insensitive.
        """
        order_exists = False
        attempt = 1 
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total__iexact=grand_total,
                    original_bag=bag,
                    stripe_pid =pid
                )
                """
                If the order is found we'll set order exists to true,
                and return a 200 HTTP response to stripe, with the message that we verified the order already exists.
                """
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt +=1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already exists in database',
                status=200)
        else:
            order = None
            try:
                """
                Also, we don't have a form to save in this webhook to create the order
                but we can do it just as easily with order.objects.create
                using all the data from the payment intent                
                """
                order = Order.Objects.create(
                        full_name=shipping_details.name,
                        email=billing_details.email,
                        phone_number=shipping_details.phone,
                        country=shipping_details.address.country,
                        postcode=shipping_details.address.postal_code,
                        town_or_city=shipping_details.address.city,
                        street_address1=shipping_details.address.line1,
                        street_address2=shipping_details.address.line2,
                        county=shipping_details.address.state,
                        original_bag=bag,
                        stripe_pid =pid
                         
                    )
                """
                We'll still want to iterate through the bag items, the only difference here is
                that we're going to load the bag from the JSON version in the payment intent
                instead of from the session.
                """
                for item_id, item_data in json.loads(bag).items():
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
            except Exception as e:
                if order: 
                    order.delete()
                return HttpResponse(
                        content=f'Webhook received: {event["type"]} | ERROR: {e}',
                        status= 500)


        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    
    def handle_payment_intent_payment_failed(self, event):
        """
        handle payment.intent.payment_failed webhooks from stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)





"""
Handle payment succeeded, explained

create a simple variable called attempt and set it to 1.
Now let's create a while loop that will execute up to 5 times.
I'll move all this code into the loop, but now instead of creating the order if it's not found the first time.
I'll increment attempt by 1
And then use pythons time module to sleep for one second.
This will in effect cause the webhook handler to try to find the order five times over five seconds
before giving up and creating the order itself.
Now since the attempt is in a while loop though, if the order is found we should break out of the loop.
Now outside the loop, I'll check whether order_exists has been set to true.
And if it has that's where it will return the 200 response

"""