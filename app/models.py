from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid
from django.contrib.auth import get_user_model

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, password, **extra_fields)

class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to="uploads", null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email



class CodingModel(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True, editable=False, null=False, blank=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    
    original_image = models.ImageField(upload_to="original", null=True)
    encoded_image = models.ImageField(upload_to="encoded", null=True)
    
    encoded_message = models.TextField(null=False, blank=False)
    
    decode_key = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, auto_created=True)
    
    algorithm = models.CharField(max_length=3, null=False, blank=False)
    # spreading_sequence = models.JSONField(null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class StatsModel(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True, editable=False, null=False, blank=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    coding = models.ForeignKey(CodingModel, on_delete=models.CASCADE) 
    coding_type = models.CharField(max_length=10, null=False, blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)