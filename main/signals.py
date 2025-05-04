from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Rating, TechList

@receiver(post_save, sender=Rating)
def update_techlist_rating(sender, instance, **kwargs):
    tech = instance.tech
    ratings = tech.ratings.all()
    if ratings.exists():
        average = round(sum(r.rating for r in ratings) / ratings.count(), 1)
        tech.stars = average
        tech.save()
