# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Query,FbQueryMapper,Token
from django.contrib import admin

# Register your models here.
admin.site.register(Query)
admin.site.register(FbQueryMapper)
admin.site.register(Token)