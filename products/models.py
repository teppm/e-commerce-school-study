from django.db import models

# Create your models here.

class Category(models.Model): #model for categories

    class Meta: 
        verbose_name_plural = 'Categories' #update the plural spelling of Category model in Admin view

    name = models.CharField(max_length=254) #name used for programmatic purposes
    friendly_name = models.CharField(max_length=254, null=True, blank=True) # 'friendly' name to use to display for example to customers

    def __str__(self):
        return self.name 
        '''A Python “magic method” that returns a string representation of any object.
         This is what Python and Django will use whenever a model instance needs to be coerced and displayed as a plain string.
          Most notably, this happens when you display an object in an interactive console or in the admin.
          You’ll always want to define this method; the default isn’t very helpful at all.'''

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL) #foreign key to a category model
    sku = models.CharField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2) 
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)


    def __str__(self):
        return self.name 
