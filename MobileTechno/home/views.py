from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    print('amin ahamdi')
    template_name = "home/home.html"

# Create your views here.
