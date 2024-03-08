from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django_filters.views import FilterView
from django.views.generic import DetailView, ListView, TemplateView, CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

from . import models
from . import filters
from . import forms


# Home page view
class HomeView(FilterView):

    model = models.Property
    context_object_name = 'properties'
    template_name = "rater/index.html"

    paginate_by = 10
    filterset_class = filters.PropertyFilter

    queryset = models.Property.objects.prefetch_related('images').all()


# Property detail view: display a property and its reviews
class PropertyDetailView(DetailView):

    model = models.Property
    context_object_name = 'property'
    template_name = 'rater/property.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        property_id = self.object.id
        context["reviews"] = models.Review.objects \
            .select_related("user") \
            .select_related("reply") \
            .filter(
            property_id=property_id)
        return context


# About page view
class AboutView(TemplateView):
    template_name = 'rater/about.html'


# Sign up view: display sign up form and register a user through post request
class SignUpView(CreateView):
    template_name = 'rater/signup.html'
    form_class = forms.SignUpForm
    success_url = reverse_lazy("signin")

    # def form_valid(self, form):
    #     form.send_email()
    #     return super().form_valid(form)


# Add Property View
class AddPropertyView(CreateView):
    template_name = 'rater/add-property.html'
    form_class = forms.PropertyForm
    success_url = reverse_lazy("home")

    # associate property with user
    def form_valid(self, form):
        user = self.request.user

        form.instance.user = user
        return super().form_valid(form)
