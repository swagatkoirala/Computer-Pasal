from django.shortcuts import redirect,render
from django.views import View
from django.urls import reverse_lazy, reverse

from store.models.customer import Customer
from store.models.orders import Order
from store.models.product import Product


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        # import pdb;pdb.set_trace()
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}
        

        # import pdb;pdb.set_trace()
        # context={"order":order}

        return redirect('cart')

# class EsewaRequestView(View):
   
#     def get(self, request, *args, **kwargs):
#         cart = request.session.get('cart')
#         # customer_id = request.session.get('customer')
#         order = Order.get_orders_by_customer(list(cart.keys()))
#         # import pdb;pdb.set_trace()
#         print(str(order))
#         import pdb;pdb.set_trace()
#         # for order in orders:

            

         
#         # o_id= request.GET.get("order.id")

#         # customer = request.session.get('customer')
#         # cart = request.session.get('cart')
#         # import pdb;pdb.set_trace()
#         order = Order.objects.get(id=order_id)
#         # import pdb;pdb.set_trace()
#         context = {
#             "order": order
#         }
#         return render(request, "esewarequest.html", context)


# class EsewaVerifyView(View):
#     def get(self, request, *args, **kwargs):
#         import xml.etree.ElementTree as ET
#         oid = request.GET.get("oid")
#         amt = request.GET.get("amt")
#         refId = request.GET.get("refId")

#         url = "https://uat.esewa.com.np/epay/transrec"
#         d = {
#             'amt': amt,
#             'scd': 'epay_payment',
#             'rid': refId,
#             'pid': oid,
#         }
#         resp = requests.post(url, d)
#         root = ET.fromstring(resp.content)
#         status = root[0].text.strip()

#         order_id = oid.split("_")[1]
#         order_obj = Order.objects.get(id=order_id)
#         if status == "Success":
#             order_obj.payment_completed = True
#             order_obj.save()
#             return redirect("/")
#         else:

#             return redirect("/esewa-request/?o_id="+order_id)


# class CheckoutView(EcomMixin, CreateView):
#     template_name = "checkout.html"
#     form_class = CheckoutForm
#     success_url = reverse_lazy("ecomapp:home")

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated and request.user.customer:
#             pass
#         else:
#             return redirect("/login/?next=/checkout/")
#         return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cart_id = self.request.session.get("cart_id", None)
#         if cart_id:
#             cart_obj = Cart.objects.get(id=cart_id)
#         else:
#             cart_obj = None
#         context['cart'] = cart_obj
#         return context

#     def form_valid(self, form):
#         cart_id = self.request.session.get("cart_id")
#         if cart_id:
#             cart_obj = Cart.objects.get(id=cart_id)
#             form.instance.cart = cart_obj
#             form.instance.subtotal = cart_obj.total
#             form.instance.discount = 0
#             form.instance.total = cart_obj.total
#             form.instance.order_status = "Order Received"
#             del self.request.session['cart_id']
#             pm = form.cleaned_data.get("payment_method")
#             order = form.save()
#             if pm == "Khalti":
#                 return redirect(reverse("ecomapp:khaltirequest") + "?o_id=" + str(order.id))
#             elif pm == "Esewa":
#                 return redirect(reverse("ecomapp:esewarequest") + "?o_id=" + str(order.id))
#         else:
#             return redirect("ecomapp:home")
#         return super().form_valid(form)


class KhaltiRequestView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        order = Order.objects.get(id=o_id)
        context = {
            "order": order
        }
        return render(request, "khaltirequest.html", context)


class KhaltiVerifyView(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        amount = request.GET.get("amount")
        o_id = request.GET.get("order_id")
        print(token, amount, o_id)

        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
        }
        headers = {
            "Authorization": "Key test_secret_key_f59e8b7d18b4499ca40f68195a846e9b"
        }

        order_obj = Order.objects.get(id=o_id)

        response = requests.post(url, payload, headers=headers)
        resp_dict = response.json()
        if resp_dict.get("idx"):
            success = True
            order_obj.payment_completed = True
            order_obj.save()
        else:
            success = False
        data = {
            "success": success
        }
        return JsonResponse(data)


class EsewaRequestView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        order = Order.objects.get(id=o_id)
        context = {
            "order": order
        }
        return render(request, "esewarequest.html", context)


class EsewaVerifyView(View):
    def get(self, request, *args, **kwargs):
        import xml.etree.ElementTree as ET
        oid = request.GET.get("oid")
        amt = request.GET.get("amt")
        refId = request.GET.get("refId")

        url = "https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': amt,
            'scd': 'epay_payment',
            'rid': refId,
            'pid': oid,
        }
        resp = requests.post(url, d)
        root = ET.fromstring(resp.content)
        status = root[0].text.strip()

        order_id = oid.split("_")[1]
        order_obj = Order.objects.get(id=order_id)
        if status == "Success":
            order_obj.payment_completed = True
            order_obj.save()
            return redirect("/")
        else:

            return redirect("/esewa-request/?o_id="+order_id)

