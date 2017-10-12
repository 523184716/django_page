# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response,render,HttpResponse
from django.shortcuts import render
from  .models import  Host
# Create your views here.
from  .common import try_int
from django.utils.safestring import mark_safe
from app01.htmlhelper import Html_page,PageInfo
def Index(request,page):
    # if request.method == "POST":
    #     print '2222'
    #     # page_item = request.POST.get('data')
    #     page_item = 10
    #     # print request.POST
    #     # print page_item
    #     # return  HttpResponse('ok')
    # else:
    #     page_item = 5
    # try:
    #
    #     page_item = request.GET.get('data')
    #     if int(page_item):
    #         page_item = int(page_item)
    # except Exception,e:
    #     page_item = 20
    # print page_item
    page_item = try_int(request.COOKIES.get('per_itme',10),10)
    page = try_int(page,1)
    count = Host.objects.all().count()
    pageinfoobj = PageInfo(page,count,page_item)
    result = Host.objects.all()[pageinfoobj.start:pageinfoobj.end]
    page_string = Html_page(page,pageinfoobj.all_page_count)
    ret = {'data':result,'count':count,'page':page_string}
    response = render_to_response('app01/index.html',ret)
    #response.set_cookie('per_itme',page_item)
    return  response

# def First_Page(request):
#     if request.method == "POST":
#         page_item = request.POST.get('data')
#         print page_item
#
#         page = try_int(page,1)
#         #page_itme = 10
#         count = Host.objects.all().count()
#
#         pageinfoobj = PageInfo(page,count,page_item)
#         result = Host.objects.all()[pageinfoobj.start:pageinfoobj.end]
#
#         page_string = Html_page(page,pageinfoobj.all_page_count)
#         ret = {'data':result,'count':count,'page':page_string}
#         return  render_to_response('app01/index.html',ret)
