"""
URL configuration for RentRater project.
"""
from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path("property/<int:pk>/", views.PropertyDetailView.as_view(), name="property"),
    path("post/", views.AddPropertyView.as_view(), name="add_property"),
    path("update/<int:pk>/", views.UpdatePropertyView.as_view(),
         name="update_property"),
    path("claim/<int:property_id>/", views.ClaimPropertyView.as_view(),
         name="claim_property"),

    path("review/", views.CreateReviewView.as_view(),
         name="create_review"),

    path("reply/", views.CreateReplyView.as_view(),
         name="create_reply"),

    path('about/', views.AboutView.as_view(), name="about"),

    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.CustomLoginView.as_view(template_name='rater/signin.html'), name='signin'),
    path('signout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('home')), name='signout'),
]
