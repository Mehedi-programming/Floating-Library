from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
import random, datetime
from django.contrib.auth.hashers import make_password
import hashlib
from django.utils import timezone


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def generate_otp()->str:
   return str(random.randint(10000, 99999))

def hash_otp(otp)->str:
   string_otp = str(otp)
   return (hashlib.sha256(string_otp.encode()).hexdigest())
   

def otp_expired(minutes=5):
   return timezone.now() + datetime.timedelta(minutes=minutes)

