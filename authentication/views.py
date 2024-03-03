from django.shortcuts import render
from django.views import *
from django.http import *
from .models import *
from django.contrib import messages
from django.urls import reverse 

# Create your views here.
def login(request):
    if request.method == "GET":
        return render(request, template_name="login.html", context={"title": "Login"})
    elif request.method == "POST":
        return render(request, template_name="login.html", context={"title": "Login"})


def register(request):
    return render(request, template_name="register.html", context={"title": "Register"})


def forgotPassword(request):
    return render(request, template_name="forgotPassword.html", context={"title": "Forgot Password"})


def resetPassword(request):
    if request.method == "GET":
        return render(request, template_name="resetPassword.html", context={"title": "Reset Password"})
    elif request.method == "POST":
        return render(request, template_name="resetPassword.html", context={"title": "Reset Password"})
        # return HttpResponsePermanentRedirect(reverse("auth.login"))


def dashboard(request):
    return render(request, template_name="dashboard.html", context={"title": "Dashboard"})


def index(request):
    # return HttpResponseServerError(content="Saday Kol Koi Data Nai")
    return render(request, template_name="index.html", context={"title": "Index"})