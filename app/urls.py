
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="auth.login"),
    path('register/', views.RegisterView.as_view(), name="auth.register"),
    path('logout/', views.LogOutView.as_view(), name="auth.logout"),
    
    path('forgot/', views.ForgotPasswordView.as_view(), name="auth.forgot"),
    path('reset/', views.PasswordResetConfirmView.as_view(), name="auth.reset"),
    
    path('profile/', views.ProfileView.as_view(), name="auth.profile"),
    
    path('dashboard/', views.DashboardView.as_view(), name="app.dashboard"),
    path('encode/', views.EncodedFilesView.as_view(), name="app.encode"),
    path('encode/list', views.EncodedFilesListView.as_view(), name="app.encode.list"),
    path('decode/', views.DecodeFilesView.as_view(), name="app.decode"),
    
    path("", views.index, name="app.index")
]
