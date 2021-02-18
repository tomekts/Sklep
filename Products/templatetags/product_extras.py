from django import template

register = template.Library()

@register.simple_tag
def my_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)


    if urlencode:
        quer = urlencode.split('&')

        filter_query = filter(lambda p: p.split('=')[0]!=field_name, quer)

        encoded = '&'.join(filter_query)
        url = '{}&{}'.format(url, encoded)

    return url