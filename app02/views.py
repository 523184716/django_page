# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from  django.shortcuts import render_to_response,redirect
# Create your views here.
from  django.template.context import RequestContext
from django.template.context_processors import csrf

##导入跨站请求伪造局部生效的两个方法
from  django.views.decorators.csrf import csrf_exempt,csrf_protect
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
def  Index(request):
    try:
        user_dict = request.session['is_login']
        if user_dict:
            #user = request.session.get['is_login']
            return render_to_response('app02/index.html',user_dict)
        else:
            return  redirect('/app02/login/')
    except Exception,e:
        return redirect('/app02/login/')
def Loginout(request):
    try:
        del request.session['is_login']
    except Exception,e:
        pass
    return redirect('/app02/login/')