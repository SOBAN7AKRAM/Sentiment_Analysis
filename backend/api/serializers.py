from rest_framework import serializers
from .models import CustomUser, EmailVerification
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'allow_blank': False}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

        
class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ["email", "otp", "created_at", "expired_at", "is_verified"]
        
    def create(self, validated_data):
        email_verification= EmailVerification.objects.update_or_create(
            email = validated_data['email'],
            defaults={
                'otp': validated_data['otp'],
                'expired_at': validated_data['expired_at'],
            }
        )
        return email_verification
        
    def verify_otp(self, email, otp):
        try:
            instance = EmailVerification.objects.get(email = email)
            if instance.otp == otp and instance.expired_at > timezone.now():
                instance.is_verified = True
                instance.save()
                return instance
            else:
                raise serializers.ValidationError("Invalid or Expired OTP")
        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError("Email not found")
