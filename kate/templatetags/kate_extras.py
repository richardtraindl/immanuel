from django import template
import datetime
from kate.engine2.match import *
from kate.engine2 import helper

register = template.Library()

@register.filter(name='imgsrc')
def imgsrc(value):
    return "img/" + value + ".png"

@register.filter(name='invert')
def invert(value):
    return int(value) ^ 1

@register.filter(name='iseven')
def iseven(count):
    return ((count % 2) == 0)

@register.filter(name='chesscnt')
def chesscnt(count):
    return ((count + 1) // 2)

@register.filter(name='matchlevel')
def matchlevel(level):
    return helper.reverse_lookup(cMatch.LEVELS, level)

@register.filter(name='matchstatus')
def matchstatus(status):
    return helper.reverse_lookup(cMatch.STATUS, status)

@register.filter(name='fmtdate')
def fmtdate(value):
   return value.strftime("%Y-%m-%d")

@register.filter(name='fmttime')
def fmttime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hour, minutes = divmod(minutes, 60)
    return "%02d:%02d:%02d" % (hour, minutes, seconds)

@register.filter(name='readmeta') 
def readmeta(value):
    return value[0]

@register.filter(name='readfield') 
def readfield(value):
    return value[1]
