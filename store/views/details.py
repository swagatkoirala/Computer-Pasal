from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View


# Create your views here.

class Details(View):
    def get(self, request):
        context = {}
        return render(request, 'product-details.html', context)

