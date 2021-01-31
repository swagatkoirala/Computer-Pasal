from django import forms
from store.models import Order , Rating

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [ "address",
                  "phone"]
    # import pdb;pdb.set_trace()
 
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields=['product','customer','score']


