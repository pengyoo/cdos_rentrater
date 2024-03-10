from django.db import models
from django.contrib.auth.models import User


# Customized User Model
class UserProfile(models.Model):

    avatar_url = models.URLField()
    profile = models.CharField(max_length=255)

    # All users are tanants but only verified user could be landlord
    is_landlord = models.BooleanField(default=False)

    # One to one relationship with the django build-in User model
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self) -> str:
        return self.user.username


# Image Model
class Image(models.Model):

    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField()
    sort = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['sort']


# Property Model
class Property(models.Model):

    eircode = models.CharField(
        max_length=10, unique=True, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='properties')
    landlord = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='my_properties', null=True, blank=True)
    address = models.TextField()
    area = models.CharField(max_length=30)
    property_type = models.CharField(max_length=50)

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
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)

    images = models.ManyToManyField(Image, blank=True)

    def __str__(self):
        return self.address

    class Meta:
        ordering = ['-created_at']


# Review Model
class Review(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.PROTECT, related_name='reviews')
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='reviews')
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.review[:50] + '...'

    class Meta:
        ordering = ['created_at']


# Reply Model
class Reply(models.Model):
    review = models.OneToOneField(Review, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.reply[:50] + '...'


# Claim Ownership Model: a landlord can claim that he owns a property
class Claim(models.Model):

    eircode = models.CharField(
        max_length=10, unique=False, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='claims')

    created_at = models.DateTimeField(auto_now_add=True)

    ownership_proof = models.OneToOneField(
        Image, on_delete=models.CASCADE, null=True, blank=True)

    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.property.eircode

    class Meta:
        ordering = ['-created_at']
