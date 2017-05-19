from django import template
import datetime
from kate.models import Match
from kate.engine import helper

register = template.Library()

@register.filter(name='imgsrc')
def imgsrc(value):
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

@register.filter(name='times') 
def times(number):
    return range(number)

@register.filter(name='reverse_times') 
def reverse_times(number):
    return range((number - 1), -1, -1)

@register.filter(name='x_coord')
def x_coord(value):
    return chr(value + ord('a'))

@register.filter(name='y_coord')
def y_coord(value):
    return chr(value + ord('1'))

@register.filter(name='field_x') 
def field_x(value):
    return (value * 4)

@register.filter(name='field_y') 
def field_x(value):
    return (value * 32)

@register.filter(name='readfield') 
def readfield(value, arg):
    pos = int(arg)
    return value[pos:(pos+3)]


