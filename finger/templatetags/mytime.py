from django import template

register = template.Library()

@register.filter
def h_m(value):
    ta = int(value)
    h = ta // 60
    m = ta % 60
    t =  '%2d : %2d' % (h,m)
    return t
@register.filter
def Time_is_ok(value):
    if value < 420:
        return True
    else:
        return False

@register.filter
def Ais(value):
    if value == 'Y':
        return False
    else:
        return True