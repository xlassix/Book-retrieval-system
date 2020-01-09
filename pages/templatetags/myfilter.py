from django import template
from django.forms.models import model_to_dict
from django.db.models import Count
from collections import Counter
register = template.Library()
@register.filter
def value_count(h,name):
    print(name)
    return list(map(lambda x:model_to_dict(x)[name],h))
@register.filter
def vcount(h,var):
    print([h.count(var)])
    return h.count(var)

"""            {
            name: '{{i}}',
            {% with var1=content_pages|value_count:"sign_in_status"|vcount:i %}
            data: {{varl}}
            {%endwith%}
        }"""
@register.filter
def value_count_values(h,name):
    print(Counter(list(map(lambda x:model_to_dict(x)[name],h))))
    return [dict(Counter(list(map(lambda x:model_to_dict(x)[name],h)))).values]

@register.filter
def makeset(h, id):
    return sorted(set(map(lambda x:model_to_dict(x)[id],h)))
@register.filter
def headerlist(h,id):
    return list(model_to_dict(h[0]).keys())[int(id):]
@register.filter
def valuelist(h,id):
    return list(model_to_dict(h).values())[int(id):]