#!/usr/bin/env python
#coding:utf-8
#from  django.middleware.csrf import  CsrfViewMiddleware
from  django.http.response import HttpResponse
from  django.shortcuts import render_to_response
from django.utils.deprecation import MiddlewareMixin

##中间件在settings中导入，请求时自上而下，返回时自下而上,
##先自上而下所有第一个process_request,然后是所有process_view,再次是url映射到views做逻辑处理
##若中间某一个process_request设置了其他方法，比如下面的做了过滤，满足条件的话会直接跳过后面的所有
##直接进入到这个中间件process_responset方法
class FilterAddress(MiddlewareMixin):
    def process_request(self,request):
        print "process_request"
        IPaddr = request.META['REMOTE_ADDR']
        # if IPaddr == "127.0.0.1":
        #     return render_to_response('error404.html')

    def process_view(self,request, view_func, view_args, view_kwargs):
        print "process_view"

    def process_exception(self,request,exception):
        print "process_exception"

    def process_response(self,request,response):
        print "process_response"
        return  response


class FilterAddress2(MiddlewareMixin):
    def process_request(self,request):
        print "2process_request"

    def process_view(self,request, view_func, view_args, view_kwargs):
        print "2process_view"

    def process_exception(self,request,exception):
        print "2process_exception"

    def process_response(self,request,response):
        print "2process_response"
        return  response