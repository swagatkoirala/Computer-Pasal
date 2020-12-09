from django.shortcuts import render
from django.views import View

from store.models import Product


class Wishlist(View):
    def get(self, request):
        products = Product.get_all_products()
        print(products)
        return render(request, 'wishlist.html', {'products': products})
