from django.template import Library
from polls.models import Map
register = Library()


@register.inclusion_tag("polls/include/map.html", takes_context=True)
def display_map(context, map, maps_js_included=False):
    if context.get('maps_js_included'):
        maps_js_included = True
    else:
        context['maps_js_included'] = True
    if isinstance(map, int):
        map = Map.objects.get(id=map)
    return {"map": map, 'STATIC_URL': context['STATIC_URL'], 'maps_js_included': maps_js_included}



