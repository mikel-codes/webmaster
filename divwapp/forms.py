#-*- coding:utf-8 -*-
import re
from django import forms 

from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from PIL import Image
from io import StringIO
from django.core.files.storage import default_storage as storage
from django.core.validators import validate_email, RegexValidator
from .models import Post, Category, UserProfile


class MessageForm(forms.Form):
    recipient = forms.ModelChoiceField(label=_("Recipient"),
            queryset=User.objects.all(),required=True)

    message   = forms.CharField(label=_("Message"), widget=forms.Textarea)
    def __init__(self, request, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.request = request 
        self.fields['recipient'].queryset = \
                self.fields["recipient"].all.exclude(pk=request.user.pk)
    def save(self):
        cleaned_data = self.cleaned_data
        send_mail(
                subject=ugettext("A message from %s")% request.user,
                message = cleaned_data["message"],
                from_email = request.user.email,
                recipient_list=[
                    cleaned_data["recipient"].email
                    ],
                fail_silently=True
                )
        pass 
        pass 


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control reginput", "autofocus":'true'}),
        required=True)
    last_name  = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control reginput"}),required=True)
    username   =  forms.CharField(widget=forms.TextInput(attrs={"class":"form-control reginput"}),required=True)
    password1  = forms.CharField(label=_('Password'),widget=forms.PasswordInput(attrs={"class":"form-control reginput"}))
    password2  = forms.CharField(label=_('Confirm Password'),widget=forms.PasswordInput(attrs={"class":"form-control reginput"}))
    email = forms.EmailField(max_length=200, help_text='Required', required=True,widget=forms.EmailInput(attrs={"class":" form-control reginput"}))

    class Meta:
        model  = User
        fields = ("first_name", "last_name", "username", "password1", "password2", "email")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        email = email.lower()
        find_mail = None
        # find a user to match for the email
        try:
            find_mail = User.objects.get(email=email)
        except Exception as e:
            pass 
        else:
            if find_mail:
                raise forms.ValidationError("Email is already in use")
        return email
      
        

class ResetPasswordForm(SetPasswordForm):
    """helps to autogenerate change password  form"""
    pass

class PostForm(forms.ModelForm):
    """ create a form to generate Posts"""
    category = forms.ModelChoiceField(queryset=Category.objects.all(),initial="Please select")
    content  = forms.CharField(min_length=100, widget=forms.Textarea(attrs={"class":"form-control"}))
    header1  = forms.CharField(validators=[RegexValidator(regex=r'^[\w\s_\d\.\&]+$', message="Invalid characters used")],
                             required=False, widget=forms.TextInput(attrs={'class':"form-control round-form"}), help_text='please use letters or numbers or _',)
    post_by= forms.ModelChoiceField(label=_("Author"), widget=forms.HiddenInput, queryset=User.objects.all(),required=False, initial='p')
    topic  = forms.CharField(validators=[RegexValidator(regex=r'^[\w\s_\d\.\&]+$', message="Invalid characters used")],
                             required=False, widget=forms.TextInput(attrs={'class':"form-control round-form"}), help_text='please use letters or numbers or _',)
    photos = forms.ImageField(label=_("Select an Image to Upload"), help_text='required field')
    links  = forms.URLField(label=_('Add your http link'), required=False, widget=forms.TextInput(attrs={"class":"form-control round-form"}), help_text="for video download or youtube link"
        )

    class Meta:
        model = Post
        fields = ("category","topic", "header1", "content", "photos", 'links', 'post_by')

    def clean_photos(self):
        image_field = self.cleaned_data.get('photos')
        try:
            image_file = StringIO(image_field.read())
        
            image = Image.open(image_file)
            w, h  = image.size
            image = image.resize((w/2, h/2), Image.ANTIALIAS)
            image_file = StringIO.StringIO()

            image.save(image_file, 'JPEG', quality=90)
            image_field.file = image_file
        except Exception as e:
            pass
        return image_field

    



            


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(), max_length=100, help_text='use less than 101 characters')
    class Meta:
        model = UserProfile
        fields = ('bio','picture')
        error_messages = {
        'max_length': "Exceed limit of characters(limit: 100)"
        }

    def clean_picture(self):
        image_field = self.cleaned_data.get('picture')
        try:
            image_file = StringIO.StringIO(image_field.read())
            
            image = Image.open(image_file)
            w, h  = image.size
            image = image.resize((100, 100), Image.ANTIALIAS)
            image_file = StringIO.StringIO()

            image.save(image_file, 'JPEG', quality=90)
            image_field.file = image_file
        except Exception as e:
                pass
        return image_field

class MultiEmailField(forms.Field):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
            return value.split(',')
    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for email in value:
            validate_email(email)



class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True)
    full_name = forms.CharField(required=True)
    company = forms.CharField(required=True)
    phone = forms.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number")],
                             required=True)
    sender_email = forms.EmailField(label=_("Your Email"), required=True)
    message = forms.CharField(label=_("Message"),required=True, widget=forms.Textarea())

    def save(self):
        cleaned_data = self.cleaned_data
        try:
            EmailMessage(
                subject=ugettext("DivWEB:: A message from %s") % cleaned_data['full_name'],
                message = ("%s \n Company Name =:> %s \n Phone: %s") % (cleaned_data["message"], cleaned_data['company'], cleaned_data['phone']),
                to=['gatezdomain@gmail.com']).send()
        except BadHeaderError:
            raise forms.ValidationError("Invalid Header Found")
            



        

