# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import  Category, Post, UserProfile
# Register your models here.


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(UserProfile)
