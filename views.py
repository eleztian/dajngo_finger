from json import *
import simplejson
from django.shortcuts import render
from django.http import HttpResponse

def test(request):
    s = request.POST.get('text')
    b = request.POST.get('b')
    t = '001123456'
    
    return HttpResponse('hello %d %s %s' % (len(str(s)) / 3,s,b))
