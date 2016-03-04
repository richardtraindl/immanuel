from django import template
from kate.models import Match
from kate.modules import values

register = template.Library()

@register.filter(name='imgsrc')
def imgsrc(value):
    piece = values.reverse_lookup(Match.PIECES, value)
    return "img/" + piece + ".png"

@register.filter(name='alternate')
def alternate(value):
    if value == 'white':
        return 'black'
    else:
        return 'white'

@register.filter(name='invert')
def invert(value):
    return int(value) ^ 1

@register.filter(name='cut')
def cut(value):
    if(len(value) == 2):
        return str(value)[1]
    else:
        return str("")

@register.filter(name='lower')
def lower(value):
    return value.lower()

    # {{ somevariable|lower:"0" }}




