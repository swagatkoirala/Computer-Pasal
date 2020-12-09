from django.core.mail import send_mail
from django.shortcuts import render
from django.views import View


# Create your views here.

class Contact(View):
    def post(self, request):
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']

        # send an email
        send_mail(
            message_name,
            message,
            message_email,
            ['joshi.ujjwal65@gmail.com']

        )

        return render(request, 'contact.html', {'message_name': message_name})

    def get(self, request):
        return render(request, 'contact.html', {})
