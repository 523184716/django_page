# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from  django.shortcuts import render_to_response,HttpResponse,redirect
# Create your views here.
from BBSchat import  models
import  json
from django.core import  serializers
import time
import  datetime
from datetime import  date
from  .common import try_int
from django.utils.safestring import mark_safe
from .htmlhelper import Html_page,PageInfo

def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print username,password
        try:
            userobj = models.Admin.objects.get(username=username)
            print userobj
        except Exception,e:
            userobj = None
        if userobj:
            request.session["user_id"] = str(userobj)
            return redirect('/bbschat/index/')
        else:
            return render_to_response('bbschat/login.html')
    return render_to_response('bbschat/login.html')

def Index(request,page):
    # page_item = try_int(request.COOKIES.get('per_itme',10),10)
    page = try_int(page,1)
    # if request.method == "POST":
    #     searchavlue = request.POST.get('searchvalue')
    #     print searchavlue
    #     count = Host.objects.filter(hostname__contains=searchavlue).count()
    #     pageinfoobj = PageInfo(page, count, page_item)
    #     result = Host.objects.filter(hostname__contains=searchavlue)[pageinfoobj.start:pageinfoobj.end]
    # else:
    count = models.NewS.objects.all().count()
    pageinfoobj = PageInfo(page, count, 3)
    result = models.NewS.objects.all()[pageinfoobj.start:pageinfoobj.end]

    page_string = Html_page(page,pageinfoobj.all_page_count)
    ret = {'data':result,'count':count,'page':page_string}
    response = render_to_response('bbschat/index.html',ret)
    #response.set_cookie('per_itme',page_item)
    return  response

# def Index(request):
#     all_data = models.NewS.objects.all()
#     return  render_to_response('bbschat/index.html',{'data':all_data})

def Add(request):
    ret = {"status":0,"data":"","message":""}
    try:
        news_id = request.POST.get('nid')
        news_obj = models.NewS.objects.get(id=news_id)
        temp = news_obj.favor_count + 1
        news_obj.favor_count = temp
        news_obj.save()
        ret["status"] = 1
        ret["data"] = temp
    except Exception,e:
        ret["status"] = 0
        ret["message"] = e.message
    return  HttpResponse(json.dumps(ret))

class CJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj,date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self,obj)

def Getrply(request):
    reply_id = request.POST.get('nid')
    reply_obj = models.Reply.objects.filter(new__id=reply_id).values('id','content','user__username','create_date')
    reply_list = list(reply_obj)
    print reply_list
    # reply_list = serializers.serialize('json',reply_obj)
    reply_list = json.dumps(reply_list,cls=CJSONEncoder)
    print reply_list
    return  HttpResponse(reply_list)


def SubmitRply(request):
    ret = {"reply_count":"","data":""}
    submit_id = request.POST.get('nid')
    submit_content = request.POST.get('data')
    new_obj = models.NewS.objects.get(id=submit_id)
    models.Reply.objects.create(
        content=submit_content,
        new = new_obj,
        user = models.Admin.objects.get(username=request.session["user_id"])
    )
    temp  = new_obj.reply_count + 1
    new_obj.reply_count = temp
    new_obj.save()
    reply_obj = models.Reply.objects.filter(content=submit_content).values('id', 'content', 'user__username', 'create_date')
    reply_list = list(reply_obj)
    reply_list = json.dumps(reply_list, cls=CJSONEncoder)
    ret["reply_count"] = temp
    ret["data"] = reply_list
    return HttpResponse(json.dumps(ret))

def Submitchat(request):
    ret = {"status":"","data":"","message":""}
    try:
        chat_content = request.POST.get("data")
        current_obj = models.Chat.objects.create(
            content = chat_content,
            user = models.Admin.objects.get(username=request.session["user_id"])
        )
        ret["status"] = 0
        ret['data']={"id":current_obj.id,"content": current_obj.content, "user": current_obj.user.username,"create_date":current_obj.crete_date.strftime("%Y-%m-%d %H:%M:%S")}
    except Exception,e:
        ret["status"] = 1
        ret["message"] = e.message
    return HttpResponse(json.dumps(ret))

def Getchat(request):
    chatnew_obj = models.Chat.objects.all().order_by("-id")[0:10].values("id","user__username","content","crete_date")
    chatnew_obj = list(chatnew_obj)
    ret = json.dumps(chatnew_obj, cls=CJSONEncoder)
    return HttpResponse(ret)

def Getchatnew(request):
    lastid = request.POST.get("lastid")
    last_data = models.Chat.objects.filter(id__gt=lastid).values("id","user__username","content","crete_date")
    last_data = list(last_data)
    ret = json.dumps(last_data, cls=CJSONEncoder)
    return HttpResponse(ret)