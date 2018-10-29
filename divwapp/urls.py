#-*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url




from .views import  registration, dashboard, userlogin, userlogout, reset, create_content, page_not_found, getpost, edit_post, delete_post, activate, edit_profile, \
 contact, index, list_posts, activate, email_password_reset, password_reset_confirm


urlpatterns = [

        path("home", index, name="indexpage"),
        path("member/new", registration, name="reg"),
        path("member/login", userlogin, name="signin"),
        path("user/<str:username>", dashboard, name="dashboard" ),
        path("logout/", userlogout, name="logout"),
        path("password/reset", reset, name="reset_password"),
        path("page/new", create_content, name="new_content"),
        path("posts/edit/<int:pk>", edit_post, name="edit_post"),
        path("contact", contact, name="contact"),
        path("category/<str:cat_name>", list_posts, name="listposts"),
        path('member/login/email/password/reset', email_password_reset, name="email_reset"),

        url(r"^oops!$",page_not_found, name="page_not_found" ),

        path("home/<slug>", getpost, name="getpost"),
        path("delete/<pk>", delete_post, name='deletepost'),
        path("profile/", edit_profile, name="edit_profile"),
        url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
        url(r'^reset/password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',password_reset_confirm, name='password_reset_confirm'),
        ]