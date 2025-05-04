from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TechList

@receiver(post_save, sender=TechList)
def update_product(sender, instance, **kwargs):
    pass