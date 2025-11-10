from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from .models import *
from .utils import *
from .serializers import *
from django.contrib.auth.hashers import make_password


# Create your views here.
@api_view(['POST'])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = User(
            username=serializer.validated_data['username'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],  
            email=serializer.validated_data['email']
        )
        user.make_password(serializer.validated_data['password'])
        redirect = serializer.save()
        return Response({"message": "User successfully registered.", "data": SignUpSerializer(redirect).data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signin(request):
    serializer = signInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = authenticate(request, username=username, password=password)
    if user:
        token = get_tokens_for_user(user)
        return Response({"access token": token['access_token'], "refresh token": token['refresh_token']}, status=status.HTTP_200_OK)
    return Response ({"message":"Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)


#edit profile
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def edit_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    serializer = UpdateSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "Your updated successfully."}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    old_password = serializer.validated_data['old_password']
    new_password = serializer.validated_data['new_password']
    
    user = User.objects.get(id=request.user.id)
    if user.check_password(old_password):
        user.make_password(new_password)
        user.save()
        return Response({"message":"Password change successfully."}, status=status.HTTP_200_OK)
    return Response({"message":"Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def forgot_password(request):
    serializer = RequestResetSerializer(data=request.data)
    print("OTP:")
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    
    user = get_object_or_404(User, email=email)
    if user:
        otp = generate_otp()
        hashed_otp = hash_otp(otp)
        Otp.objects.create(
            user=user,
            otp_hash = hashed_otp,
            is_used = False,
            expired_at = otp_expired()
        )
        print("OTP is:", otp)
        # send_sms(otp)
        return Response({"message": "OTP send seccessfully."}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def verify_otp(request):
    serializer = VerifyOtpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    otp = serializer.validated_data['otp']
    
    try:
        user = User.objects.get(email=email)
        otp_obj = Otp.objects.filter(user=user, is_used=False).first()
    except User.DoesNotExist:
        return Response({"message": "User doesn't exist."}, status=status.HTTP_308_PERMANENT_REDIRECT)
    if otp_obj.expired_at < timezone.now():
        return Response({"message": "OTP expired."}, status=status.HTTP_400_BAD_REQUEST)
    if otp_obj.otp_hash != hash_otp(otp):
        return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
    
    otp_obj.is_used = True
    otp_obj.save()
    return Response({"message": "Your OTP is valid."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    try:
        user = User.objects.get(email=email)
    except Exception as e :
        return Response({"detail": "Invalid reset token"}, status=status.HTTP_400_BAD_REQUEST)
    user.password = make_password(password)
    user.save()
    return Response ({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
