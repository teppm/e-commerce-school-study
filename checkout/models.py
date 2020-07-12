import uuid #used to create order number

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField

from profiles.models import UserProfile
from products.models import Product


# Create your models here.

class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False) #basic character field, max lent 32char, created automatically, cannot be edited
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True,
                                     blank=True, related_name='orders') # use models.SET_NULL if the profile is deleted since that will allow us to keep an order history in the admin even if the user is deleted.
    full_name = models.CharField(max_length=50, null=False, blank=False) # name chat field, 50 char, required
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True) # null and false true as not mandatory
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)  # address 1 mandatory
    street_address2 = models.CharField(max_length=80, null=True, blank=True) # address 2 not mandatory
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True) #add date and timestamp to purchases
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default="")
    stripe_pid = models.CharField(max_length=24, null=False, blank=False, default="")



    def _generate_order_number(self): #underscore before generate is a convention that indicates that this method is only used in this class
        """
        generates a random unique order number using UUID  (uuid4 is used for random 32 hex string)
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        update grand total each time line item is added, accounting for delivery costs
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE/100
        else: 
            self.delivery_cost = 0
            
        self.grand_total = self.order_total + self.delivery_cost
        self.save()
        """
        The way this works is by using the sum function across all the line-item total fields for all line items on this order.
        The default behaviour is to add a new field to the query set called line-item total sum.
        Which we can then get and set the order total to that.
        """
        

    def save(self, *args, **kwargs):
        """
        override the original save method to set the order number if it hasnt been set
        """
        if not self.order_number: #if no order number exists
            self.order_number = self._generate_order_number() #call _generate function to creat one
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number
    

class OrderLineItem(models.Model):
    """A line-item will be like an individual shopping bag item. Relating to a specific order
    And referencing the product itself. The size that was selected. The quantity.
    And the total cost for that line item.
    The basic idea here. Is when a user checks out.
    We'll first use the information they put into the payment form to create an order instance.
    And then we'll iterate through the items in the shopping bag.
    Creating an order line item for each one. Attaching it to the order.
    And updating the delivery cost, order total, and grand total along the way."""

    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems') #There's a foreign key to the order. With a related name of line items.So when accessing orders we'll be able to make calls such as order.lineitems.all and order.lineitems.filter
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE) #There's also a foreign key to the product for this line item.So that we can access all the fields of the associated product as well.
    product_size = models.CharField(max_length=2, null=True, blank=True) #XS,S,M,L,XL sizes, can be left blank as not all products have sizes
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'

    
    