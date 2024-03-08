from django.db import models
from django.contrib.auth.models import User


# Customized User Model
class UserProfile(models.Model):

    avatar_url = models.URLField()
    profile = models.CharField(max_length=255)

    # All users are tanants but only verified user could be landlord
    is_landlord = models.BooleanField(default=False)

    # One to one relationship with the django build-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)


# Image Model
class ImageModel(models.Model):

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    url = models.URLField()
    sort = models.IntegerField()

    class Meta:
        ordering = ['sort']


# Property Model
class PropertyModel(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='properties')
    address = models.TextField()
    area = models.CharField(max_length=30)
    property_type = models.CharField(max_length=50)
    room_type = models.CharField(max_length=50)

    GENDER_CHOICES = (
        ('B', 'Male/Female'),
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender_preference = models.CharField(max_length=1, choices=GENDER_CHOICES)
    owner_occupied = models.BooleanField(default=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # average rating
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    images = models.ManyToManyField(ImageModel)

    class Meta:
        ordering = ['created_at']


# Review Model
class ReviewModel(models.Model):
    property = models.ForeignKey(
        PropertyModel, on_delete=models.PROTECT, related_name='reviews')
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='reviews')
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# Reply Model
class ReplyModel(models.Model):
    review = models.OneToOneField(ReviewModel, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
