from django.contrib import admin
from . import models

# Register models.
admin.site.register(models.UserProfile)
admin.site.register(models.Image)
admin.site.register(models.Property)
admin.site.register(models.Review)
admin.site.register(models.Reply)
admin.site.register(models.Claim)
