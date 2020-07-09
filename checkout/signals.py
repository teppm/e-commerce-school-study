"""
from django.db.models.signals import post_save, post_delete  -->
So this implies these signals are sent by django to the entire application
after a model instance is saved and after it's deleted respectively.
To receive these signals we can import receiver from django.dispatch.
"""

from django.db.models.signals import post_save, post_delete 
from django.dispatch import receiver


from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    This is a special type of function which will handle signals from the post_save event.
    So these parameters refer to the sender of the signal. In our case OrderLineItem.
    The actual instance of the model that sent it.
    A boolean sent by django referring to whether this is a new instance or one being updated.
    And any keyword arguments.
    """
    """
    update order total on lineitem update/creat
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    update order total on lineitem delete
    """
    instance.order.update_total()