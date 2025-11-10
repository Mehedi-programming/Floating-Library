from .models import *
from rest_framework import serializers



class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

class signInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

class RequestResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=4, write_only = True)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only= True)