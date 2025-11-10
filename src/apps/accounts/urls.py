from django.urls import path
from . views import *
from . models import *

urlpatterns = [
    path('signup/', sign_up, name='sign_up'),
    path('signin/', signin, name='signin'),
    path('change-password/', change_password, name='change_password'),
    path('edit-profile/<int:user_id>/', edit_profile, name='edit_profile'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('reset-password/', reset_password, name='reset_password'),
]
