from django.shortcuts import render
from django.views import View

# Create your views here.
from django.views.generic import DetailView

from store.models import Product, Category


class Details(DetailView):
    model = Product
    template_name = "product-details.html"

