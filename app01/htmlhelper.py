#/usr/bin/env python
#coding:utf-8
from django.utils.safestring import mark_safe

class PageInfo:
    def __init__(self,curren_page,all_count,per_item=5):
        self.CurrenPage = curren_page
        self.AllCount = all_count
        self.PerItem = per_item

    @property
    def start(self):
        return (self.CurrenPage-1) * self.PerItem
    @property
    def end(self):
        return self.CurrenPage * self.PerItem
    @property
    def all_page_count(self):
        temp = divmod(self.AllCount,self.PerItem)
        if temp[1]:
            all_page_count = temp[0] + 1
        else:
            all_page_count = temp[0]
        return all_page_count

def Html_page(page,all_page):
    '''
    :param page: 当前页
    :param all_page: 总页数
    :return:
    '''
    page_html = []
    start_html = '<a href="/app01/index/%d">首页</a>' % (1)
    page_html.append(start_html)
    if page <= 1:
        pre_html = '<a href="#">上一页</a>'
    else:
        pre_html = '<a href="/app01/index/%d">上一页</a>' % (page-1)
    page_html.append(pre_html)
    if all_page < 12:
        start_page = 0
        end_page = all_page
    else:
        if page < 6:
            start_page = 0
            end_page = 11
        else:
            if page+5 > all_page:
                start_page = all_page - 11
                end_page = all_page
            else:
                start_page = page - 6
                end_page = page + 5

    for i in range(start_page,end_page):
        if page == i+1:
            a_html = "<a class='selected' href='/app01/index/%d'>%d</a>" % (i + 1, i + 1)
        else:
            a_html = '<a href="/app01/index/%d">%d</a>' % (i+1,i+1)
        page_html.append(a_html)
    if page >= all_page:
        nex_html = '<a href="#">下一页</a>'
    else:
        nex_html = '<a href="/app01/index/%d">下一页</a>' % (page+1)
    page_html.append(nex_html)
    end_html = '<a href="/app01/index/%d">尾页</a>' % (all_page)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string
