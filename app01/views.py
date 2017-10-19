# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response,render,HttpResponse
from django.shortcuts import render
from  .models import  Host
# Create your views here.
from  .common import try_int
from django.utils.safestring import mark_safe
from app01.htmlhelper import Html_page,PageInfo
from   django.views.decorators.csrf import csrf_exempt,csrf_protect

@csrf_exempt
def Index(request,page):
    page_item = try_int(request.COOKIES.get('per_itme',10),10)
    page = try_int(page,1)
    if request.method == "POST":
        searchavlue = request.POST.get('searchvalue')
        print searchavlue
        count = Host.objects.filter(hostname__contains=searchavlue).count()
        pageinfoobj = PageInfo(page, count, page_item)
        result = Host.objects.filter(hostname__contains=searchavlue)[pageinfoobj.start:pageinfoobj.end]
    else:
        count = Host.objects.all().count()
        pageinfoobj = PageInfo(page, count, page_item)
        result = Host.objects.all()[pageinfoobj.start:pageinfoobj.end]

    page_string = Html_page(page,pageinfoobj.all_page_count)
    ret = {'data':result,'count':count,'page':page_string}
    response = render_to_response('app01/index.html',ret)
    #response.set_cookie('per_itme',page_item)
    return  response

def Filter(befor_fun,after_fun):
    def outer(main_func):
        def wrapper(request,*args,**kwargs):
            befor_result = befor_fun(request)
            if befor_result != None:
                return  befor_result
            main_result = main_func(request)
            if main_result != None:
                return main_result
            after_result = after_fun(request)
            if after_result != None:
                return  after_result
        return  wrapper
    return  outer

def befor_fun(request):
    print "befor_fun"

def after_fun(request):
    print "after_fun"
    return HttpResponse("ok")

@Filter(befor_fun,after_fun)
def DecratorTest(request):
    print "DecratorTest"