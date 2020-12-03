from django.urls import path

from .middlewares.auth import auth_middleware
from .views.about import About
from .views.cart import Cart
from .views.checkout import CheckOut
from .views.contact import Contact
from .views.home import Index, store
from .views.login import Login, logout
from .views.orders import OrderView
from .views.signup import Signup
from .views.start import Start
from .views.details import Details

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('start', Start.as_view(), name='start'),
    path('store', store, name='store'),
    path('about', About.as_view(), name='about'),
    path('contact', Contact.as_view(), name='contact'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('cart', auth_middleware(Cart.as_view()), name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('product-details', Details.as_view(), name='product-details'),
]
