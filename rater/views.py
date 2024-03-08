from django.shortcuts import render
from django.views.generic.list import ListView


class HomeView(ListView):
    def get(self, request):
        return render(request, 'rater/index.html')
