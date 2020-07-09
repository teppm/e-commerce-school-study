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
            content=f'Webhook received: {event["type"]}',
            status=200)