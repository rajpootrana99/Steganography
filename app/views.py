
import json
from django.utils.timezone import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LogoutView, PasswordResetConfirmView, PasswordChangeView
from django.http import *

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image  # Make sure to install the Pillow library if not already installed

from django.contrib import messages # for showing or throwing validation errors
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from .models import *
from .forms import RegistrationForm, LoginForm, UserBioUpdateForm, UserPasswordChangeForm, EncodingForm, DecodingForm
from .map import ALGO_MAP
from steganography.settings import BASE_DIR
import os, uuid

from django.db.models import Count
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
import humanize

# creating class based template views
class LoginView(View):
    
    def get(self, request):
        form = LoginForm(request) # default django provides Authentication Form
        
        return render(request, template_name="login.html", context={"form": form})
    
    def post(self, request):
        # handling form submission
        form = LoginForm(data=request.POST)
        
        if form.is_valid(): # all credentials are correct
            user = form.get_user() # getting current user models which is going to logged in
            login(request, user) # logging current user in
            
            # by default django sessions last two weeks
            if not form.cleaned_data.get("remember_me"): # if not checked
                request.session.set_expiry(0) # set short time when user haven't selected remember me option
                
            return redirect("app.dashboard") # redirecting to dashboard
        
        print(form.errors)
        # return form with the errors
        return render(request, template_name="login.html", context={"form": form})
        # return HttpResponsePermanentRedirect(reverse("auth.login"))

# creating registration view
class RegisterView(View):
    
    def get(self, request):
        form = RegistrationForm() # custom created Registration Form in forms.py
        
        return render(request, template_name="register.html", context={"form": form})
    
    def post(self, request):
        
        # form submitted by user
        form = RegistrationForm(data=request.POST)
        
        
        if form.is_valid(): # all fields contained valid data
            user = form.save()
            login(request, user) # logging current user in
            request.session.set_expiry(0) # set short time when user haven't selected remember me option
            return redirect("app.dashboard") # redirecting to dashboard
        
        print(form.errors.as_json())
        # return form with the errors
        return render(request, template_name="register.html", context={"form": form})
        
# creating logout 
class LogOutView(LogoutView):
    next_page = "/login"

class ForgotPasswordView(View):
    def get(self, request):
        
        return render(request, template_name="forgotPassword.html", context={"title": "Forgot Password"})
        
    def post(self, request):
        
        return render(request, template_name="forgotPassword.html", context={"title": "Forgot Password"})
        
# creating Password Reset Confirm View
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'resetPassword.html'
    success_url = reverse_lazy('/login')
    form_class = SetPasswordForm
    post_reset_login = True

    
# creating user update view
class ProfileView(LoginRequiredMixin, View):
    login_url= "/login"
    
    def get(self, request):
        bio_form = UserBioUpdateForm(instance=request.user)
        pass_change_form = UserPasswordChangeForm(user=request.user)
        initial_type = "bio"
        
        return render(request, template_name="profile.html", context={"bioForm" : bio_form, "passForm": pass_change_form, "formType": initial_type})
    
    def post(self, request):
        initial_type = None
        bio_form = UserBioUpdateForm(instance=request.user)
        if request.POST["type"] == "bio":
            bio_form = UserBioUpdateForm(request.POST, request.FILES, instance=request.user)
            initial_type = "bio"
            
            if bio_form.is_valid():    
                
                if request.FILES.get("profile_image", None) is not None:
                    # print(request.user)
                    print(request.POST["previous_image"])
                    if request.POST["previous_image"] != "":
                        
                        image_path = os.path.join(BASE_DIR, 'media/' + request.POST["previous_image"]).replace("\\", "/")
                        
                        print(image_path)
                        if os.path.isfile(image_path):
                            os.remove(image_path)
                        
                bio_form.save()
                messages.success(request, "Your profile updated successfully!")
            print(bio_form.errors.as_json())
        
        pass_change_form = UserPasswordChangeForm(user=request.user)
        if request.POST["type"] == "password":
            pass_change_form = UserPasswordChangeForm(request.user, request.POST)
            initial_type = "password"
            if pass_change_form.is_valid():
                user = pass_change_form.save()
                update_session_auth_hash(request, user)
                pass_change_form = UserPasswordChangeForm(user=request.user)
                messages.success(request, "Your password updated successfully!")
            print(pass_change_form.errors.as_json())
            
        if initial_type == None: 
            initial_type = "bio"
        
        return render(request, template_name="profile.html", context={"bioForm" : bio_form, "passForm": pass_change_form, "formType": initial_type})

class EncodedFilesView(LoginRequiredMixin, View):
    login_url= "/login"
    
    def get(self, request):
        form = EncodingForm()
        return render(request, template_name="encode.html", context={"form": form})

    def post(self, request):
        form = EncodingForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            
            instance.user = request.user
            instance.save()
            
            
            # saving in stats model
            stat = StatsModel.objects.create(
                user = request.user,
                coding = instance,
                coding_type = "encode"
            )
            stat.save()
            
            algorithm = instance.algorithm
            
            actual_file_name = instance.original_image.name.replace("original/", "")
            print(actual_file_name)
            # Now that the instance is saved, we can access the path of the original_image
            save_path = os.path.join(BASE_DIR, "media/" + instance.original_image.name.replace("original", "algo_generated")).replace("\\", "/")
            original_path = os.path.join(BASE_DIR, "media/" + instance.original_image.name).replace("\\", "/")
            print(save_path)

            if algorithm == "SS":
                ALGO_MAP["SS"]["encode"](original_path, instance.encoded_message, save_path)
            else:
                ALGO_MAP[algorithm]["encode"](original_path, instance.encoded_message, save_path)

            # Additional processing before saving if needed
            encoded_image_path = save_path
            # Open the encoded image file and save it to the ImageField
            with open(encoded_image_path, 'rb') as encoded_image_file:
                # Create a Django File from the file
                django_file = SimpleUploadedFile(encoded_image_path, encoded_image_file.read())

                # Save the Django File to the ImageField
                instance.encoded_image.save(actual_file_name, django_file, save=False)
            
            print(instance)
            instance.save()
            
            
            if os.path.isfile(save_path):
                os.remove(save_path)
            
            
            return redirect('app.encode.list')  # Redirect to a success page or any other page after successful form submission

        return render(request, template_name="encode.html", context={"form": form})

class EncodedFilesListView(LoginRequiredMixin, View):
    login_url= "/login"
    
    def get(self, request):
        encoded_list = CodingModel.objects.filter(user=request.user).order_by("-created_at")
        # print(encoded_list)
        return render(request, template_name="encodeList.html", context={"files": encoded_list})
    
    # def post(self, request):
    #     return render(request, template_name="encodeList.html", context={"title": "Encode Files List"})
    
class DecodeFilesView(LoginRequiredMixin, View):
    login_url= "/login"
    
    def get(self, request):
        form = DecodingForm()
        return render(request, template_name="decode.html", context={"form": form})
    
    def post(self, request):
        form = DecodingForm(request.POST, request.FILES)
        
        if form.is_valid():
            key = form.cleaned_data.get("key")
            algorithm = form.cleaned_data.get("algorithm")
            
            encoded = CodingModel.objects.filter(decode_key=key).first()
            encoded_image_path = os.path.join(BASE_DIR, "media/" + encoded.encoded_image.name).replace("\\", "/")
            
            decoded_message = ALGO_MAP[algorithm]["decode"](encoded_image_path)
            
            # saving in stats model
            stat = StatsModel.objects.create(
                user = request.user,
                coding = encoded,
                coding_type = "decode"
            )
            stat.save()
            
            messages.success(request, decoded_message)
            
        
        print(form.errors)
        return render(request, template_name="decode.html", context={"form": form})


class DashboardView(LoginRequiredMixin, View):
    login_url= "/login"
    
    def get(self, request):
        total_encodes = StatsModel.objects.filter(user=request.user, coding_type = "encode").count()
        total_decodes = StatsModel.objects.filter(user=request.user, coding_type = "decode").count()
        
        # Example for total decodes grouped by each day
        decode_stats_line_array = [0] * 6
        decode_stats = StatsModel.objects.filter(coding_type='decode',
            user=request.user).annotate(
            day=TruncDate('created_at')
        ).values('day').annotate(
            total_decodes=Count('id')
        ).order_by('day')
        total_decode_past_six_days = 0
        i = 5
        for stat in decode_stats[:6]:
            decode_stats_line_array[i] = stat["total_decodes"]
            total_decode_past_six_days += stat["total_decodes"]
            i -= 1

        # Example for total encodes grouped by each day
        encode_stats_line_array = [0] * 6
        encode_stats = StatsModel.objects.filter(coding_type='encode',
            user=request.user).annotate(
            day=TruncDate('created_at')
        ).values('day').annotate(
            total_encodes=Count('id')
        ).order_by('day')
        
        total_encode_past_six_days = 0
        i = 5
        for stat in encode_stats[:6]:
            encode_stats_line_array[i] = stat["total_encodes"]
            total_encode_past_six_days += stat["total_encodes"]
            i -= 1
            
        # getting data for percentage based circular graph
        # Get the current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year
        monthly_stats = StatsModel.objects.filter(
            created_at__month=current_month,
            created_at__year=current_year,
            user=request.user
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month', 'coding_type').annotate(
            total_files=Count('id')
        ).order_by('month')
        per_month_encoding = 0
        per_month_decoding = 0
        total_month_coding = 0
        for stat in monthly_stats:
            if stat["coding_type"] == "encode":
                per_month_encoding += stat["total_files"]
            else:
                per_month_decoding += stat["total_files"]
                
            total_month_coding += stat["total_files"]
        
        # print(monthly_stats)
        
        # Example for encoding and decoding counts grouped by year and month
        yearly_stats = StatsModel.objects.filter(user=request.user).annotate(
            year=TruncYear('created_at'),
            month=TruncMonth('created_at')
        ).values('year', 'month', 'coding_type').annotate(
            total_files=Count('id')
        ).order_by('-year', 'month')

        # Organize the data in the desired format
        result_data = {}
        all_years = list()

        for stat in yearly_stats:
            year_str = str(stat['year'].year)
            if year_str not in all_years:
                all_years.append(year_str)
            month_str = str(stat['month'].month)

            if year_str not in result_data:
                result_data[year_str] = {'Encode': [0] * 12, 'Decode': [0] * 12}

            if stat['coding_type'] == 'encode':
                result_data[year_str]['Encode'][int(month_str) - 1] = stat['total_files']
            elif stat['coding_type'] == 'decode':
                result_data[year_str]['Decode'][int(month_str) - 1] = stat['total_files']
        else:
            all_years.append(str(current_year))
            result_data = {
                str(current_year):{
                    'Encode': [0] * 12,
                    'Decode': [0] * 12
                }
            }
        
        print(result_data)
        
        
        context = {
            "total_users": UserModel.objects.all().count(),
            "total_coding": total_encodes+total_decodes,
            "total_encodes": total_encodes,
            "total_decodes": total_decodes,
            "decode_stats": decode_stats,
            "encode_stats": encode_stats,
            "total_encode_past_six_days": total_encode_past_six_days,
            "total_decode_past_six_days": total_decode_past_six_days,
            "encode_stats_line": encode_stats_line_array,
            "decode_stats_line": decode_stats_line_array,
            "total_month_coding": total_month_coding,
            "coding_percentage": [(int(per_month_encoding/total_month_coding * 100) if total_month_coding != 0 and per_month_encoding != 0 else 0),(int(per_month_decoding/total_month_coding * 100) if total_month_coding != 0 and per_month_decoding != 0 else 0)],
            "all_years": all_years,
            "report_data": result_data
        }
        
        # print(context)
        # print(encoded_list)
        return render(request, template_name="dashboard.html", context=context)
    
    


def index(request):
    return render(request, template_name="index.html", context={"title": "Index"})