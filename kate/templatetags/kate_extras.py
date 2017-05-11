from django import template
import datetime
from kate.models import Match
from kate.engine import helper

register = template.Library()

@register.filter(name='imgsrc')
def imgsrc(value):
    piece = helper.reverse_lookup(Match.PIECES, value)
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

@register.filter(name='letter')
def letter(value):
    return chr(value + ord('A'))

@register.filter(name='lower')
def lower(value):
    return value.lower()

@register.filter(name='iseven')
def iseven(count):
    return ((count % 2) == 0)

@register.filter(name='chesscnt')
def chesscnt(count):
    return ((count + 1) // 2)

@register.filter(name='matchlevel')
def matchlevel(level):
    return helper.reverse_lookup(Match.LEVELS, level)

@register.filter(name='booltoint')
def booltoint(value):
    if(value):
        return 1
    else:
        return 0

@register.filter(name='fmtdate')
def fmtdate(value):
   return value.strftime("%Y-%m-%d")

