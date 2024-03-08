from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django_filters.views import FilterView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from . import models
from . import filters


class HomeView(FilterView):

    model = models.Property
    context_object_name = 'properties'
    template_name = "rater/index.html"

    paginate_by = 2
    filterset_class = filters.PropertyFilter

    queryset = models.Property.objects.prefetch_related('images').all()


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


class AboutView(TemplateView):
    template_name = 'rater/about.html'
