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
from django.core.files.storage import default_storage as storage

NAME_CHOICE = (
         ("MR", "Mr"), 
         ("MRS","Mrs"),
         ("MISS","Miss"),
         )

POST_IMG_SIZE = getattr(settings, "POST_SIZE", (50, 50))
PROFILE_SIZE  = getattr(settings, "PROFILE_IMG_SIZE", (100, 100))
# Create your models here.
def storagedir(instance, uploadedfile):
    now=timezone_now()
    filename, filetype = os.path.splitext(uploadedfile)
    return "images/webpics/%s%s" % (now.strftime("%Y/%m/%Y%m%d%H%M%S"), filetype.lower())

def photo_storagedir(instance, uploadedfile):
    now = timezone_now()
    file, file_ext = os.path.splitext(uploadedfile)
    return "images/profile_pics/%s%s" % (now.strftime("%Y/%m/%Y%m%d%H%M%S"), file_ext.lower())
     
    

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
    header1  = models.CharField(_("First Heading"), max_length=255, unique=True, null=True, blank=True)
    content  = models.TextField(_("Content"), max_length=10000)
    slug     = models.SlugField(unique=True, null=True, blank=True)
    photos   = models.ImageField(upload_to=storagedir)
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
    picture  =  models.ImageField(upload_to=photo_storagedir, blank=True, null=True)

    def __str__(self):
        return self.author.get_full_name()
    








