# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from  django.shortcuts import render_to_response,redirect
# Create your views here.
from  django.template.context import RequestContext
from django.template.context_processors import csrf

##导入跨站请求伪造局部生效的两个方法
from  django.views.decorators.csrf import csrf_exempt,csrf_protect

def checklogin(func):
    def wrapper(request,*args,**kwargs):
        try:
            print request.session['is_login']
            if  request.session['is_login']:
                return func(request,*args,**kwargs)
            else:
                print 33333
                return redirect('/app02/login/')
        except Exception, e:
            print e
            print 2222
            return redirect('/app02/login/')
    return wrapper

def Login(request):
    print "views.login"
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        user = request.POST.get('username',None)
        pwd = request.POST.get('password',None)
        print user,pwd
        if user == 'ceshi' and pwd == 'ceshi':
            request.session['is_login'] = {'user':user}
            return  redirect('/app02/index/')
        else:
            ##django 1.8.2
            return render_to_response('app02/login.html',{'status':"用户名和密码不对"},c)
            ##之前版本
            #return render_to_response('app02/login.html', {'status': "用户名和密码不对"}, context_instance=RequestContext(request))
    return render_to_response('app02/login.html',c)

# @csrf_protect   #当全局没有设置跨站请求伪造保护时，加上这个装饰器可以强制加上这个功能
# @csrf_exempt    #当全局有开启跨站请求伪造保护时，设置这个可以让这个方法强制取消
@checklogin
def  Index(request,*args,**kwargs):
    print 11111
    print args[0]
    #print kwargs['page']
    return render_to_response('app02/index.html')

def Loginout(request):
    try:
        del request.session['is_login']
    except Exception,e:
        pass
    return redirect('/app02/login/')