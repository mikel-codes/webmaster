#-*- coding:utf-8 -*-
from django.conf.urls import url




from .views import  registration, dashboard, userlogin, userlogout, reset, create_content, page_not_found, getpost, edit_post, delete_post, activate, edit_profile, \
 contact, index, list_posts, activate, email_password_reset, password_reset_confirm


urlpatterns = [

        url(r"^home$", index, name="indexpage"),
     
        url(r"^user/new$", registration, name="reg"),
        url(r"^user/login$", userlogin, name="signin"),
        url(r"^user/(?P<pk>\w+)$", dashboard, name="dashboard" ),
        url(r"^logout/", userlogout, name="logout"),
        url(r"^password/reset$", reset, name="reset_password"),
        url(r"^page/new$", create_content, name="new_content"),
        url(r"^posts/edit/(?P<pk>\d+)", edit_post, name="edit_post"),
        url(r"^contact$", contact, name="contact"),
        url(r"^category/(?P<pk>[A-Za-z\&\s]+)$", list_posts, name="listposts"),
        url(r"^oops!$",page_not_found, name="page_not_found" ),
        url(r"^home/(?P<pk>[0-9A-Za-z_\-\s]+)$", getpost, name="getpost"),
        url(r"^delete/(?P<pk>\d+)$", delete_post, name='deletepost'),
        url(r"^profile/$", edit_profile, name="edit_profile"),
        url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
        url(r'^reset/password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',password_reset_confirm, name='password_reset_confirm'),
        url(r'^user/login/email/password/reset$', email_password_reset, name="email_reset")
        ]