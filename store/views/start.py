from django.shortcuts import render
from django.views import View

from store.models.category import Category
from store.models.product import Product

# Create your views here.

class Start(View):
    def get(self, request):
        context = {}
        return render(request, 'start.html', context)



