from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django_filters.views import FilterView
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView
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


# Update Property View
class UpdatePropertyView(UpdateView):
    template_name = 'rater/update-property.html'
    form_class = forms.PropertyForm
    model = models.Property
    context_object_name = "property"
    success_url = reverse_lazy("home")


# Claim Property View
class ClaimPropertyView(CreateView):
    template_name = 'rater/claim-property.html'
    form_class = forms.ClaimForm
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        property = models.Property.objects.get(
            pk=self.kwargs['property_id'])
        address = property.address
        eircode = property.eircode

        kwargs['initial']['address'] = address
        kwargs['initial']['eircode'] = eircode
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ClaimPropertyView, self).get_context_data(**kwargs)
        context['property_id'] = self.kwargs.get('property_id')
        return context

    # associate claim with property and user
    def form_valid(self, form):
        user = self.request.user
        property_id = self.get_context_data()['property_id']
        property = models.Property.objects.get(pk=property_id)
        form.instance.user = user
        form.instance.property = property
        return super().form_valid(form)


# Create Review View
class CreateReviewView(CreateView):
    form_class = forms.ReviewForm
    success_url = reverse_lazy("home")

    # associate review with property and user
    def form_valid(self, form):
        user = self.request.user
        property_id = form.cleaned_data.get('property_id')
        property = models.Property.objects.get(pk=property_id)
        form.instance.user = user
        form.instance.property = property
        return super().form_valid(form)
