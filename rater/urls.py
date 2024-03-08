"""
URL configuration for RentRater project.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path("property/<int:pk>/", views.PropertyDetailView.as_view(), name="property"),
    path('about/', views.AboutView.as_view(), name="about"),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', auth_views.LoginView.as_view(template_name='rater/signin.html'), name='signin'),
    path('signout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('home')), name='signout'),
]
