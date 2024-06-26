from typing import Any
from urllib.parse import urlparse
from django.db.models.query import QuerySet
from django.shortcuts import render
from django_filters.views import FilterView
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.http import HttpResponseRedirect

from uuid import uuid4
import os

from . import models
from . import filters
from . import forms


from .utils import upload_file

LOGIN_URL = '/signin/'


def redirect(url):
    """ Controll redirect urls """
    if not url.startswith("http") and not url.startswith("https"):
        return HttpResponseRedirect(url)
    parsed_url = urlparse(url)
    if parsed_url.netloc in settings.ALLOWED_HOSTS:
        return HttpResponseRedirect("https://" + parsed_url.netloc)
    return HttpResponseRedirect("/")


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


class CustomLoginView(LoginView):
    authentication_form = forms.CustomAuthenticationForm

    def form_valid(self, form):
        redirect_to = self.request.POST.get('next')
        response = super().form_valid(form)
        if redirect_to:
            return redirect(redirect_to)
        else:
            return response


# Add Property View
class AddPropertyView(LoginRequiredMixin, CreateView):
    login_url = LOGIN_URL
    redirect_field_name = "next"
    template_name = 'rater/add-property.html'
    form_class = forms.PropertyForm

    # Process image upload and relationships with other objects
    def form_valid(self, form):

        # associate current with property
        user = self.request.user
        form.instance.user = user

        # Upload image
        image = form.cleaned_data.get("image")
        object_name = settings.S3_IMAGE_PATH + \
            str(uuid4()) + os.path.splitext(image.name)[1].lower()
        image_url = upload_file(image, object_name)

        # Save image object
        image_saved = models.Image.objects.create(
            title=os.path.splitext(image.name)[0], url=image_url)

        # save property before associate it with image (many-to-many)
        return_value = super().form_valid(form)

        # associate image with property
        form.instance.images.add(image_saved)

        return return_value

    # echo form data if data is invalid
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    # redirect to published property
    def get_success_url(self):
        return reverse_lazy('property', kwargs={'pk': self.object.pk})


# Update Property View
class UpdatePropertyView(LoginRequiredMixin, UpdateView):
    login_url = LOGIN_URL
    redirect_field_name = "next"
    template_name = 'rater/update-property.html'
    form_class = forms.PropertyForm
    model = models.Property
    context_object_name = "property"
    success_url = reverse_lazy("home")


# Claim Property View
class ClaimPropertyView(LoginRequiredMixin, CreateView):
    login_url = LOGIN_URL
    redirect_field_name = "next"
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

    def get_success_url(self):
        return reverse_lazy('property', kwargs={'pk': self.object.property.pk})


# Create Review View
class CreateReviewView(LoginRequiredMixin, CreateView):
    login_url = LOGIN_URL
    redirect_field_name = "next"

    form_class = forms.ReviewForm

    # associate review with property and user
    def form_valid(self, form):
        user = self.request.user
        property_id = form.cleaned_data.get('property_id')
        property = models.Property.objects.get(pk=property_id)
        form.instance.user = user
        form.instance.property = property
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('property', kwargs={'pk': self.object.property.pk})


# Create Reply View
class CreateReplyView(LoginRequiredMixin, CreateView):
    login_url = LOGIN_URL
    redirect_field_name = "next"

    form_class = forms.ReplyForm

    # associate review with property and user
    def form_valid(self, form):
        user = self.request.user
        review_id = form.cleaned_data.get('review_id')
        review = models.Review.objects.get(pk=review_id)
        form.instance.user = user
        form.instance.review = review
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('property', kwargs={'pk': self.object.review.property.pk})
