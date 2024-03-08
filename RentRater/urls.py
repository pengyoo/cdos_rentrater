"""
URL configuration for RentRater project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rater/', include('rater.urls')),
]
