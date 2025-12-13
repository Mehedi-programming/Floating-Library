from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomerUserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False) 
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    is_lender = models.BooleanField(default=False)
    is_borrower = models.BooleanField(default=False)

    objects = CustomerUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ['-id']


class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    otp_hash = models.CharField(max_length=255)
    expired_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.user.name}"
    
    class Meta:
        ordering = ['-created_at']
        
