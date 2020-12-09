from django.shortcuts import render
from django.views import View

from store.models import Product


class Search(View):
    def get(self, request):
        query = request.GET.get('search')
        products = Product.objects.filter(name__icontains=query)
        return render(request, 'search.html', {'products': products})
