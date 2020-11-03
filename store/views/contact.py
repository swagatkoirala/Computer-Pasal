from django.shortcuts import render
from django.views import View


# Create your views here.

class Contact(View):
    def get(self, request):
        context = {}
        return render(request, 'contact.html', context)
