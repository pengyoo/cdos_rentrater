from django.contrib import admin
from . import models
from django.utils.html import format_html

# Register models.
admin.site.register(models.UserProfile)
admin.site.register(models.Claim)

# Custimize display fields for Image model


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']

    def image(self, image):
        return format_html('<img src="{}" class="thumbnail"/>',
                           image.url)

    class Media:
        css = {
            'all': ['rater/css/styles.css']
        }


# Custimize display fields for Property model
@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['image', 'area', 'address', 'eircode', 'user', 'landlord']

    def image(self, property):
        return format_html('<img src="{}" class="thumbnail"/>',
                           property.images.first().url)

    class Media:
        css = {
            'all': ['rater/css/styles.css']
        }


# Custimize display fields for Review model
@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review', 'rating', 'user']


# Custimize display fields for Reply model
@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['reply', 'user']
