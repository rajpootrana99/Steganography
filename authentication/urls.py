
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="auth.login"),
    path('register/', views.register, name="auth.register"),
    path('forgot/', views.forgotPassword, name="auth.forgot"),
    path('reset/', views.resetPassword, name="auth.reset"),
    path('dashboard/', views.dashboard, name="app.dashboard"),
    path("", views.index, name="app.index")
]
