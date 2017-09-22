# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
    return render(request,'nav.html')

def order_vis(request):
    return render(request,'order_vis.html')

def fee_vis(request):
    return render(request,'fee_vis.html')

def inv_vis(request):
    return render(request,'inv_vis.html')

def inv_mon_vis(request):
    return render(request,'inv_mon_vis.html')

def jump_to_load(request):
    
    return HttpResponse(u"success")

def upload(request):
    return HttpResponse(u"success")