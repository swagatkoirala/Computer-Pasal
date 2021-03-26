from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .customer import Customer
from .product import Product

class Rating (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,default=0)
    score = models.IntegerField ( default=0,
                                  validators=[
                                      MaxValueValidator ( 5 ),
                                      MinValueValidator ( 0 ),
                                  ]
                                  )
    # slug = models.SlugField()

    # def get_absolute_url(self):
    #     return reverse("rating", kwargs={
    #         'slug': self.slug
    #     })


    def __str__(self):
        return str ( self.product )
    def RateSubmit(self):
        self.save()