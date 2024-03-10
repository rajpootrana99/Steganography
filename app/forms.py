from typing import Any
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import *

from .map import ALGO_MAP

class DecodingForm(forms.Form):
    encoded_image = forms.ImageField(widget=forms.FileInput(), label="Encoded Image", required=True)
    key = forms.UUIDField(label="Key", widget=forms.TextInput())
    algorithm = forms.CharField(label="Algorithm")
    
    def clean_encoded_image(self):
        image = self.cleaned_data.get('encoded_image', False)
        allowed = ALGO_MAP[self.data.get("algorithm")]["allowed"]
        key = self.data.get("key")
        if image:
            if image.size > 5*1024*1024:
                raise ValidationError("Image file too large ( > 5mb )")
            print(self.cleaned_data.get("algorithm"))
            
            # setting unique image name
            extension = image._name.split(".")[len(image._name.split("."))-1]
            
            # raise ValidationError(image_name)
            # print(allowed)
            if extension not in allowed:
                raise ValidationError(f"{('Only' if len(allowed) > 0 else 'No')} {', '.join(allowed)} extension{('s' if len(allowed) > 1 else '')} are allowed with {(self.data.get('algorithm') if self.data.get('algorithm') != 'SS' else 'Spread Spectrum')} Algorithm")
            
            encoded = CodingModel.objects.filter(decode_key=key).first()
            if encoded is None:
                raise ValidationError(f"No associated encoding record exists againt key {key}")
            
            encoded_filename = encoded.encoded_image.name.split("/")[1]
            if encoded_filename != image._name:
                raise ValidationError(f"Image \"{image._name}\" provided is not encoded image or not associated with the key {key}.")
            
        return image

class EncodingForm(forms.ModelForm):
    
    class Meta:
        model = CodingModel
        fields = ["original_image", "encoded_message", "algorithm"]
        
    
        
    
    def clean_original_image(self):
        image = self.cleaned_data.get('original_image', False)
        # print(image.__dict__)
        # print(self.cleaned_data)
        # print(self.__dict__)
        # print(self.data.get("algorithm"))
        allowed = ALGO_MAP[self.data.get("algorithm")]["allowed"]
        if image:
            if image.size > 5*1024*1024:
                raise ValidationError("Image file too large ( > 5mb )")
            print(self.cleaned_data.get("algorithm"))
            # setting unique image name
            id = str(uuid.uuid4())
            extension = image._name.split(".")[len(image._name.split("."))-1]
            
            if extension not in allowed:
                raise ValidationError(f"{('Only' if len(allowed) > 0 else 'No')} {', '.join(allowed)} extension{('s' if len(allowed) > 1 or len(allowed) == 0 else '')} are allowed with {(self.data.get('algorithm') if self.data.get('algorithm') != 'SS' else 'Spread Spectrum')} Algorithm")
            
            image._name = self.data.get("algorithm")+ "__" + id +"."+extension
            image.field_name = id
            # print(image.__dict__)
            
        return image
    


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
        # print(image.__dict__)
        if image:
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
            
    
        