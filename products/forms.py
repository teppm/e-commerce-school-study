from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):

    
    class Meta:
        model = Product
        fields = '__all__' #special dunder or double underscore string called all which will include all the fields.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories] #This special syntax is called the list comprehension.And is just a shorthand way of creating a for loop that adds items to a list

        self.fields['category'].choices =  friendly_names #Now that we have the friendly names, let's update the category field on the form.To use those for choices instead of using the id.
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'