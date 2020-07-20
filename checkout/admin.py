from django.contrib import admin
from .models import Order, OrderLineItem
# Register your models here.



class OrderLineItemAdminInline(admin.TabularInline):
    """
    Now let's add an inline admin class.
    OrderLineItemAdminInline which is going to inherit from admin.TabularInline.
    This inline item is going to allow us to add and edit line items in the admin
    right from inside the order model.
    So when we look at an order. We'll see a list of editable line items on the same page.
    Rather than having to go to the order line item interface.
    """

    model = OrderLineItem
    readonly_fields = ('lineitem_total', )

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    """
    readonly_fields -->
    These fields are all things that will be calculated by our model methods.
    Including order number, date, delivery cost, order total, and grand_total.
    So we don't want anyone to have the ability to edit them
    since it could compromise the integrity of an order.
    """
    readonly_fields = ('order_number', 'date','delivery_cost', 'order_total', 'grand_total',
                      'original_bag', 'stripe_pid')

    """
    fields -->
    I'll also use the fields option. Which isn't absolutely necessary here.
    But it will allow us to specify the order of the fields in the admin interface
    which would otherwise be adjusted by django due to the use of some read-only fields.
    This way the order stays the same as it appears in the model.
    """

    fields = ('order_number', 'user_profile ''date', 'full_name', 'email', 'phone_number',
             'country', 'postcode', 'town_or_city', 'street_address1', 'street_address2',
             'county', 'delivery_cost', 'order_total', 'grand_total', 'original_bag', 'stripe_pid')

    """
    list_display -->
    Last I'll use the list display option.
    To restrict the columns that show up in the order list to only a few key items.
    """

    list_display = ('order_number', 'date', 'full_name',
                    'delivery_cost', 'order_total',
                     'grand_total',)

    ordering = ('-date', ) #"order by date with most recent orders at the top"

admin.site.register(Order, OrderAdmin)