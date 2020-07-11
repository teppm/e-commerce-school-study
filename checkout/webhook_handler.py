from django.http import HttpResponse

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
        print(intent)
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    
    def handle_payment_intent_payment_failed(self, event):
        """
        handle payment.intent.payment_failed webhooks from stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)