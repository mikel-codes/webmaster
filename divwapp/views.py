# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from itertools import chain

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from django.http import Http404, HttpResponse 

#necessary for email confirmation
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage, send_mail, BadHeaderError



from .forms import  SignUpForm, ResetPasswordForm, PostForm, ProfileForm, ContactForm
from .tokens import account_activation_token
import random

from .models import Post, UserProfile, Category

# Create your views here.

def index(request):
    try:
        head_post = Post.objects.latest()
    except:
        head_post = None
    related_posts_first = Post.objects.filter(category=head_post.category).order_by("topic", "last_modified").exclude(pk=head_post.id)[:2]
    recipe_for_head = Post.objects.filter(pk=head_post.id)

    top_posts = Post.objects.order_by("topic", 'category','last_modified').exclude(id__in=[x.id for x in list(chain(related_posts_first, recipe_for_head))])[:3]
    recent_posts = Post.objects.all().exclude(id__in=[p.id for p in list(chain(related_posts_first, top_posts, recipe_for_head))])[:10]
    category = random.choice(Category.objects.all())
    category_posts = Post.objects.filter(category=category).order_by("last_modified", "post_by").exclude(pk=head_post.id)[:4]
    categories = Category.objects.all()
    return render(request, "index.html", locals())


def list_posts(request, cat_name=None):
    category = get_object_or_404(Category, name=cat_name)
    posts_by_category = Post.objects.filter(category=category)
    head_post = Post.objects.all().first()  
    categories = Category.objects.all()
    return render(request, "website/category_posts.html", locals())

def getpost(request, slug=None):
    req_post = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.filter(category=req_post.category).exclude(pk=req_post.id)[:6]
    recipe_for_req = Post.objects.filter(pk=req_post.id)
    posts    = Post.objects.all().exclude(id__in=[c.id for c in list(chain(related_posts, recipe_for_req))])[:5]
    categories = Category.objects.all()
    head_post = Post.objects.all().first()
    last_p = Post.objects.latest()
    try:
        profile = get_object_or_404(UserProfile, pk=req_post.post_by)
    except:
        profile="Anonymous"
    return render(request, "website/requested_post.html", locals())


def contact(request):
    categories = Category.objects.all()
    form = ContactForm()
    if request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Message Sent")        
            return redirect(reverse("contact"))
    context = {"form": form, "categories": categories}
    return render(request, 'website/contact.html', context)

def email_password_reset(request):
    email = request.POST.get('email', '')
    try:
       user = User.objects.get(email=email)
       if user and user.is_active:
        message = render_to_string("activate_reset_password.html", {
            "email" : email,
            "domain" : get_current_site(request).domain,
            "uid" : urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            "token" : account_activation_token.make_token(user)
        })

        mail = EmailMessage("Please use the Reset link ",
            message,
            to=[email],headers = {'Reply-To': 'noreply@divweb.com'}
            )
        mail.send()
    except(BadHeaderError, ValueError, Exception):
        messages.info(request,"sent link to email ")
        return redirect("signin")
    else:
        messages.info(request, "Sent Link to Email Address ")
        return redirect("signin")    

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user.is_active and account_activation_token.check_token(user, token):
        user.refresh_from_db()
        login(request, user)
        return redirect(reverse("reset_password"))
    else:
        return redirect("page_not_found")
    

def registration(request):
    if request.POST:
        signupform = SignUpForm(request.POST)
        if signupform.is_valid():
            user = signupform.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Account Activation"

            mail_message = render_to_string("activate_acct_mail.html", {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user) 
                })

            to_email = signupform.cleaned_data.get('email')
            email=EmailMessage( mail_subject, mail_message, to=[to_email] ,
                 headers = {'Reply-To': 'noreply@divweb.com'})
            email.send()
            return HttpResponse('PLEASE CHECK EMAIL FOR FURTHER INSTRUCTIONS')

    else: 
        signupform = SignUpForm()
    fterms = ("Username","Email")
    return render(request, "registration/signup.html",{"signupform": signupform, 'fterms':fterms})

def activate(request, uidb64, token):
    try:
    	uid = urlsafe_base64_decode(uidb64).decode()
    	user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
    	user.refresh_from_db()
    	user.is_active = True
    	user.save()
    	login(request, user)
    	messages.success(request,"registration completed successfully")    
    	return redirect(reverse("dashboard", args=(user.username,)))
    else:
        return redirect("page_not_found")

def userlogin(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user     = authenticate(request, username=username, password=password)
        if user is not None and user.is_active: # if the account of the user is still active
                login(request, user)
                request.session["identity"] = request.user.id 
                messages.success(request,"Welcome %s your dashboard" % request.user.username)
                return redirect(reverse('dashboard', args=(request.user.username,)))
        else:
            context = {"errors" : "login details are invalid"}
            return render(request, "registration/login.html", context)
    else:
        return render(request, "registration/login.html", {})

@login_required
def reset(request):
    if request.POST:
        form = ResetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.info(request,"Password reset is successfull")
            return redirect(reverse('dashboard', args=(request.user.username,)))
    else:
        form = ResetPasswordForm(request.user)
    return render(request, "dashboard/reset.html",{"form": form})
    pass

@login_required(login_url = "signin")
def dashboard(request,  username):
	user = get_object_or_404(User, username=username)
	posts = Post.objects.filter(post_by=user.id).order_by("-last_modified")
	count = posts.count()
	try:	
		profile = get_object_or_404(UserProfile, author=user)
	except Exception as e:
		profile = None
	context = {'post_count': count, "posts":posts, "profile":profile }
	return render(request, 'layouts/dashboard.html', context)

@login_required(login_url='signin')
def userlogout(request):
    """ simply logs out the user """
    logout(request)
    return redirect(reverse("signin"))



@login_required(login_url="signin")
def create_content(request):
    """ Create content to be displayed"""
    if request.method == "POST":
        form = PostForm(request, request.POST, request.FILES)    
        if form.is_valid():
            form.save()
            messages.info(request, "Your post was added successfully")
            return redirect(reverse("dashboard", args=(request.user.username,)))
    else:
        form = PostForm(request)
    return render(request, "dashboard/user_content.html", {'form': form, 'subvalue':"Create Post"})


@login_required(login_url='signin')
def edit_post(request, pk):
   post = get_object_or_404(Post, pk=pk)
   form = PostForm(request, request.POST or None,request.FILES or None, instance=post)
   if form.is_valid():
        form.save()
        messages.info(request, "Post is updated successfully")
        return redirect(reverse("dashboard", args=(request.user.username,)))
   return render(request, "dashboard/user_content.html", {'form': form, 'subvalue': "Update Post", "post":post})

@login_required(login_url="signin")
def delete_post(request, pk):
    try:
        post = get_object_or_404(Post, id=pk)
        post.delete()
    except Exception as e:
        return redirect("page_not_found")
    else:
        messages.info(request, "The post was successfully removed")
        return redirect("dashboard", args=(request.user.username))

@login_required(login_url="signin")
def search_posts(request):
    results = Category.objects.filter()
    pass

@login_required(login_url="signin")
def edit_profile(request):
    try:
        profile = get_object_or_404(UserProfile, pk=request.user.id)
        form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
        if form.is_valid():
            obj_form = form.save(commit=False)
            obj_form.author = request.user
            obj_form.save()
            messages.info(request, "Profile is updated successfully")
            return redirect(reverse("dashboard", args=(request.user.username,)))
    except Exception as e:
        profile=None
        form = ProfileForm()
        if request.POST:
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)
                form.author = request.user
                form.save()
                messages.info(request, "Hurray!, you now own a work profile")
                return redirect(reverse("dashboard", args=(request.user.username,)))
    return render(request, "dashboard/profile.html", {'form':form, 'legend': "edit profile", 'profile':profile})





def page_not_found(request):
    return render(request, "404.html", {})
