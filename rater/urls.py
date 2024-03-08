"""
URL configuration for RentRater project.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="properties"),
    path("property/<int:pk>/", views.PropertyDetailView.as_view(), name="property"),
    path('about/', views.AboutView.as_view(), name="about"),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
