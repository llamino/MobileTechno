from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "home/home.html"

    def context_data(self, **kwargs):
        context = self.request.User
        return context

# Create your views here.
