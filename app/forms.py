from typing import Any
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import *

from .map import ALGO_MAP

import unicodedata
from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return (
        unicodedata.normalize("NFKC", s1).casefold()
        == unicodedata.normalize("NFKC", s2).casefold()
    )


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            print(html_email)
            email_message.attach_alternative(html_email, "text/html")

        #all email settings
        print(email_message.connection)
        print(email_message.__dict__)
        
        
        
        print(email_message.send())


class DecodingForm(forms.Form):
    encoded_file = forms.FileField(widget=forms.FileInput(), label="Encoded File", required=True)
    key = forms.UUIDField(label="Key", widget=forms.TextInput())
    algorithm = forms.CharField(label="Algorithm")
    
    def clean_encoded_file(self):
        file = self.cleaned_data.get('encoded_file', False)
        allowed = ALGO_MAP[self.data.get("algorithm")]["allowed"]
        key = self.data.get("key")
        if file:
            if file.size > 5*1024*1024:
                raise ValidationError("file too large ( > 5mb )")
            print(self.cleaned_data.get("algorithm"))
            
            # setting unique image name
            extension = file._name.split(".")[len(file._name.split("."))-1]
            
            # raise ValidationError(image_name)
            # print(allowed)
            if extension not in allowed:
                raise ValidationError(f"{('Only' if len(allowed) > 0 else 'No')} {', '.join(allowed)} extension{('s' if len(allowed) > 1 else '')} are allowed with {(self.data.get('algorithm') if self.data.get('algorithm') != 'SS' else 'Spread Spectrum')} Algorithm")
            
            encoded = CodingModel.objects.filter(decode_key=key).first()
            if encoded is None:
                raise ValidationError(f"No associated encoding record exists againt key {key}")
            
            encoded_filename = encoded.encoded_file_or_folder.split("/")
            encoded_filename = encoded_filename[len(encoded_filename)-1]
            original_filename = encoded.original_file.name.split("/")
            original_filename = original_filename[len(original_filename)-1]
            print(file.__dict__)
            print(encoded_filename)
            print(original_filename)
            print(original_filename != file._name)
            if encoded_filename != file._name and original_filename != file._name:
                raise ValidationError(f"File \"{file._name}\" provided is not encoded file or not associated with the key {key}.")
            
        return file

class EncodingForm(forms.ModelForm):
    
    class Meta:
        model = CodingModel
        fields = ["original_file", "encoded_message", "algorithm"]
        
    
        
    
    def clean_original_file(self):
        file = self.cleaned_data.get('original_file', False)
        # print(image.__dict__)
        # print(self.cleaned_data)
        # print(self.__dict__)
        # print(self.data.get("algorithm"))
        allowed = ALGO_MAP[self.data.get("algorithm")]["allowed"]
        if file:
            if file.size > 5*1024*1024:
                raise ValidationError("file too large ( > 5mb )")
            print(self.cleaned_data.get("algorithm"))
            # setting unique image name
            id = str(uuid.uuid4())
            extension = file._name.split(".")[len(file._name.split("."))-1]
            
            if extension not in allowed:
                raise ValidationError(f"{('Only' if len(allowed) > 0 else 'No')} {', '.join(allowed)} extension{('s' if len(allowed) > 1 or len(allowed) == 0 else '')} are allowed with {(self.data.get('algorithm') if self.data.get('algorithm') != 'SS' else 'Spread Spectrum')} Algorithm")
            
            file._name = self.data.get("algorithm")+ "__" + id +"."+extension
            file.field_name = id
            # print(image.__dict__)
            
        return file
    


class UserBioUpdateForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(), required=True, label="Full Name")
    email = forms.EmailField(widget=forms.EmailInput(), label="Email", error_messages={
        "unique": "Email Address already in use"
    })
    profile_image = forms.ImageField(widget=forms.FileInput(), required=False, label="Profile Image")
    
    class Meta:
        model = UserModel
        fields = ["full_name", "email", "profile_image"]
    
    
    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image', False)
        print(image.__dict__)
        if image:
            # print(image)
            if image.size > 1*1024*1024:
                raise ValidationError("Image file too large ( > 1mb )")
            # setting unique image name
            id = str(uuid.uuid4())
            extension = image._name.split(".")[len(image._name.split("."))-1]
            image._name = id+"."+extension
            image.field_name = id
            # print(image.__dict__)
            
        return image
        
        
class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    new_password2 = forms.CharField(label="Retype New Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}))
    
    

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password", required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password", required=True)
    full_name = forms.CharField(widget=forms.TextInput(), required=True, label="Full Name")    

    #overriding user already exists with email unique validator message
    email = forms.EmailField(widget=forms.EmailInput(), label="Email", error_messages={
        "unique": "Email Address already in use"
    })
    
    class Meta:
        model = UserModel
        fields = ["full_name", "email", "password1", "password2"]
        
class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(), label="Email", error_messages={
        "unique": "Email Address already in use",
        "required": "Email is required",
        "invalid": "Please enter a valid email address"
    })
    
    remember_me = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
            
    
        