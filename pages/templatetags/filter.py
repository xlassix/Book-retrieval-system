from django import template
register = template.Library()
@register.filter
def multi(num,value):
    return num*value