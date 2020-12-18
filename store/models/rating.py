from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Rating (models.Model):
    score = models.IntegerField ( default=0,
                                  validators=[
                                      MaxValueValidator ( 5 ),
                                      MinValueValidator ( 0 ),
                                  ]
                                  )


    def __str__(self):
        return str ( self.pk )