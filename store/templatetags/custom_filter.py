from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter(name='currency')
def currency(numbers):
    if numbers == '' :
        numbers = round(float(0),2)
    else:
        numbers = round(float(numbers), 2)
    
    
    numbers="Rs. %s%s" % (intcomma(int(numbers)), ("%0.2f" % numbers)[-3:])
    # import pdb; pdb.set_trace()
    return numbers


@register.filter(name='multiply')
def multiply(number, number1):
    return number * number1
