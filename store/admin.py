from django.contrib import admin

from .models import Product, Category, Customer, Order, Rating

admin.site.site_header = "Computer Pasal"


@admin.register(Product)
class CustProduct(admin.ModelAdmin):
    list_display = ('name', 'category', 'brands')
    # ordering = ['-']


@admin.register(Category)
class CustCategory(admin.ModelAdmin):
    ordering = ['name']


@admin.register(Customer)
class CustCustomer(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email')
    ordering = ['first_name']


@admin.register(Order)
class CustOrder(admin.ModelAdmin):
    list_display = ('product', 'customer', 'quantity', 'address', 'date', 'status')
    ordering = ['date']

@admin.register(Rating)
class CustRating(admin.ModelAdmin):
    pass