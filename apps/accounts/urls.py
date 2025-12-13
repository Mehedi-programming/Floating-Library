from django.urls import path
from . views import *
from . models import *

urlpatterns = [
    path('signup/', sign_up, name='sign_up'),
    path('signin/', signin, name='signin'),
    path('change-password/', change_password, name='change_password'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('reset-password/', reset_password, name='reset_password'),
    path('activate-user-account/<int:user_id>/', activate_user_account, name='activate_user_account'),
    path('deactivate-user-account/<int:user_id>/', deactivate_user_account, name='deactivate_user_account'),
    path('dashboard-stats/', dashboard_stats, name='dashboard_stats'),
    path('all-user/', all_user, name='all_user'),
    path('inactive-users/', inactive_users, name='inactive_users'),
    path('active-users/', active_users, name='active_users'),
    path('my-accounts/', my_accounts, name='my_accounts')
    # path("send-email/", send_email, name="send_email"),
]
