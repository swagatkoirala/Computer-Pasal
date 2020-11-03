from django.shortcuts import render
from django.views import View


# Create your views here.

class About(View):
    def get(self, request):
        context = {}
        return render(request, 'about.html', context)
