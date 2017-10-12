# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from  django.shortcuts import render_to_response,redirect
# Create your views here.


def Login(request):
    if request.method == "POST":
        user = request.POST.get('username',None)
        pwd = request.POST.get('password',None)
        print user,pwd
        if user == 'ceshi' and pwd == 'ceshi':
            request.session['is_login'] = {'user':user}
            return  redirect('/app02/index/')
        else:
            return render_to_response('app02/login.html',{'status':"用户名和密码不对"})

    return render_to_response('app02/login.html')

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
    del request.session['is_login']
    return redirect('/app02/login/')