from django.db import models
from django.shortcuts import reverse

from .category import Category


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    brands = models.CharField(max_length=100, default='')
    slug = models.SlugField(blank=True,unique=True,default="my-slug-")
    description = models.TextField()

    image = models.ImageField(upload_to='uploads/products/')

    def get_absolute_url(self):
        return reverse("product-details", kwargs={
            'slug': self.slug
        })


    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()
    

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()
