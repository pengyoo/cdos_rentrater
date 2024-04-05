
"""
Register models to admin system

"""

from django.contrib import admin
from django.utils.html import format_html
from . import models

# Register models.
admin.site.register(models.UserProfile)


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
    list_display = ['rating', 'property_eircode', 'review', 'user', ]
    
    def property_eircode(self, review):
        return review.property.eircode



@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    """ Custimize display fields for Reply model """
    list_display = ['reply', 'user']



@admin.register(models.Claim)
class ClaimAdmin(admin.ModelAdmin):
    """ Custimize display fields for Review model """
    list_display = ['eircode', 'user', 'created_at', 'ownership_proof']
    
    def ownership_proof(self, property):
        """ display image """
        return format_html('<img src="{}" class="thumbnail"/>',property.images.first().url)

    class Media:
        """ load style files """
        css = {
            'all': ['rater/css/styles.css']
        }