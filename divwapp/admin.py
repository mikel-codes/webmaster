# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import  Category, Post, UserProfile
# Register your models here.



admin.site.register(Category)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['topic','post_by', "category"]
    list_filter = ('post_by', )
    ordering = ('topic', )
    search_fields = ('topic', )


admin.site.register(UserProfile)
