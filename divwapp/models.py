# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.db import models

# Create your models here.
from PIL import Image
from django.contrib.auth.models import User
from django.utils.timezone import now as timezone_now
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from divweb.aws_storage_backends import PrivateMediaImageStorage as pr_mis, PublicMediaImageStorage as pmis

class TimeStampsMixin(models.Model):
    last_modified = models.DateTimeField(auto_now=True)
    created_on    = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

class Category(TimeStampsMixin):
    """docstring for Category"""
    name = models.CharField(_("Category Name"), unique=True, max_length=255, blank=False, null=False)
    def __str__(self):
        return self.name
    class Meta(object):
        verbose_name="Category"
        verbose_name_plural = "Categories"
        

class Post(TimeStampsMixin):
    """docstring for Post"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    topic    = models.CharField(_("Topic"), max_length=255, unique=True)
    content  = models.TextField(_("Content"), max_length=10000)
    slug     = models.SlugField(unique=True, null=True, blank=True)
    photos   = models.ImageField(storage=pmis(), blank=False,null=False)
    post_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    
    
    class Meta:
        verbose_name='Post'
        verbose_name_plural="Posts"
        get_latest_by = "id"




    def __str__(self):
        return self.topic

    def __unicode__(self):
        return self.topic

    



class UserProfile(models.Model):
    author   =  models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                primary_key=True)
    bio      =  models.TextField(_("About Author"), max_length=100)
    picture  =  models.ImageField(storage=pr_mis(), null=True)

    def __str__(self):
        return self.author.get_full_name()
    








