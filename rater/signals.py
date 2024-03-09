from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import Avg

from .models import UserProfile, Claim, Property, Review


# Use django signals to automatically create UserProfile when a user sign up
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# Use signals to associate property with a landlord when it's verified by admin user
@receiver(post_save, sender=Claim)
def create_profile(sender, instance, created, **kwargs):
    if instance.verified:
        property = Property.objects.get(pk=instance.property.id)
        property.landlord = instance.user
        property.save()


# Use signals to calculate average rating when a user rate a property
@receiver(post_save, sender=Review)
def create_profile(sender, instance, created, **kwargs):
    if created:
        avg_rating = Review.objects.filter(property=instance.property).aggregate(
            avg_rating=Avg('rating'))['avg_rating']
        Property.objects.filter(
            pk=instance.property.id).update(rating=avg_rating)
