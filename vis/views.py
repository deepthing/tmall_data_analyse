# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import os
from django.http import HttpResponse
import tmall_data_analyse.settings as settings
import load.service as service

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
    try:
        service.loaddata(settings.BASE_FILE_PATH.get('upload_path'))
        return HttpResponse("success")
    except Exception as identifier:
        return HttpResponse("false")
    

def upload(request):
    if request.method == "POST":
        zipfile = request.FILES.get("zipfile",None)
        if not zipfile:
            return HttpResponse("empty")
        storefile = open(os.path.join(settings.BASE_FILE_PATH.get('upzip_path')),'wb+')
        for chunk in zipfile.chunks():
            storefile.write(chunk)
        storefile.close()
        
        return HttpResponse("success")
    else:
        return HttpResponse("wrong")