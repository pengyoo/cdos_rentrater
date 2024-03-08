"""
URL configuration for RentRater project.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path("property/<int:pk>/", views.PropertyDetailView.as_view(), name="property"),
]
