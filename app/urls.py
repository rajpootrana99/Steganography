
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="auth.login"),
    path('register/', views.RegisterView.as_view(), name="auth.register"),
    path('logout/', views.LogOutView.as_view(), name="auth.logout"),
    
    path('forgot/', views.ForgotPasswordView.as_view(), name="auth.forgot"),
    path('forgot/success/', views.EmailSentView.as_view(), name="auth.forgot.success"),
    
    path('reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name="auth.reset"),
    path('reset/done/', views.PasswordResetDoneView.as_view(template_name="resetDone.html"), name="auth.reset.done"),
    
    path('profile/', views.ProfileView.as_view(), name="auth.profile"),
    
    path('dashboard/', views.DashboardView.as_view(), name="app.dashboard"),
    path('encode/', views.EncodedFilesView.as_view(), name="app.encode"),
    path('encode/list', views.EncodedFilesListView.as_view(), name="app.encode.list"),
    path('decode/', views.DecodeFilesView.as_view(), name="app.decode"),
    
    path("", views.index, name="app.index"),
    # path("404/", views.error500)
]