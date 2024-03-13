import django_filters
from . import models


# http://127.0.0.1:8000/?page=1&rating__gte=5&area__contains=Citywest
class PropertyFilter(django_filters.FilterSet):
    class Meta:
        model = models.Property
        fields = {
            'rating': ['lte', 'gte'],
            'address': ['contains'],
            'user': ['exact'],
            'landlord__id': ['exact'],
        }
