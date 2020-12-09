from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter(name='currency')
def currency(numbers):
    numbers = round(float(numbers), 2)
    return "Rs. %s%s" % (intcomma(int(numbers)), ("%0.2f" % numbers)[-3:])


@register.filter(name='multiply')
def multiply(number, number1):
    return number * number1
