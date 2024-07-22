from django import template

register = template.Library()

@register.simple_tag
def active(request, url_name):
    if request.resolver_match.url_name == url_name:
        return 'active'
    return ''
