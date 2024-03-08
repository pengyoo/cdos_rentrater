from django.shortcuts import render
from django.views.generic.list import ListView
from . import models


class HomeView(ListView):
    model = models.Property
    context_object_name = 'properties'
    template_name = "rater/index.html"

    queryset = models.Property.objects.prefetch_related('images').all()
