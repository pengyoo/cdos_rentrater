
"""
Register models to admin system

"""

from django.contrib import admin
from . import models
from django.utils.html import format_html


# Register models.
admin.site.register(models.UserProfile)
admin.site.register(models.Claim)



@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    """ Custimize display fields for Image model """
    list_display = ['title', 'image']

    def image(self, image):
        """ display image """
        return format_html('<img src="{}" class="thumbnail"/>',
                           image.url)

    class Media:
        """ load style files """
        css = {
            'all': ['rater/css/styles.css']
        }



@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):
    """ Custimize display fields for Property model """
    list_display = ['image', 'area', 'address', 'eircode', 'user', 'landlord']

    def image(self, property):
        """ display image """
        return format_html('<img src="{}" class="thumbnail"/>',property.images.first().url)

    class Media:
        """ load style files """
        css = {
            'all': ['rater/css/styles.css']
        }



@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    """ Custimize display fields for Review model """
    list_display = ['review', 'rating', 'user']



@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    """ Custimize display fields for Reply model """
    list_display = ['reply', 'user']
