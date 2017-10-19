# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import NewS,UserType,Admin,NewType,Reply

admin.site.register(NewS)
admin.site.register(UserType)
admin.site.register(Admin)
admin.site.register(NewType)
admin.site.register(Reply)
