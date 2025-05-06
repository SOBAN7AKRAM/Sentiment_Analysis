from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .ml_model import predict_sentiment
from django_ratelimit.decorators import ratelimit
from cryptography.fernet import Fernet
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import numpy as np
from .models import EmailVerification
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status, serializers
from .serializers import UserCreateSerializer, EmailVerificationSerializer
import random
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

User = get_user_model()




def get_tokens_for_user(user):
    """
    Generate refresh and access tokens for a user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    
class CSRFTokenView(APIView):
    """
    Returns a CSRF token.
    """
    permission_classes = []
    
    def get(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        return Response({'csrfToken': csrf_token})

def generate_otp():
    otp = np.random.choice(range(10), size = 6)
    otp_str = ""
    for i in range(6):
        otp_str += str(otp[i])
    return otp_str

def send_otp_email(email, otp):
    subject = "OTP Code for Hire-Hive"
    message = f"Your OTP code is {otp} for Hire-Hive email verification. It is valid for 5 minutes."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        otp = generate_otp()
        expired_at = timezone.now() + timedelta(minutes=5)

        serializer = EmailVerificationSerializer(data={
            "email": email,
            "otp": otp,
            "expired_at": expired_at
        })

        if serializer.is_valid():
            serializer.save()
            send_otp_email(email, otp)  # Only send after saving
            return Response({"message": "OTP sent"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        serializer = EmailVerificationSerializer()
        try:
            result = serializer.verify_otp(email, otp)
            return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({"error": str(e.detail[0])}, status=status.HTTP_400_BAD_REQUEST)

class SignupView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Check if OTP for this email is verified
        try:
            otp_entry = EmailVerification.objects.get(email=email)
            if not otp_entry.is_verified:
                return Response({"error": "Email not verified"}, status=status.HTTP_400_BAD_REQUEST)
        except EmailVerification.DoesNotExist:
            return Response({"error": "Email verification not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        serializer = UserCreateSerializer(data={"email": email, "password": password})
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()

            # Optionally clear OTP record to prevent reuse
            otp_entry.delete()

            tokens = get_tokens_for_user(user)
            user_data = serializer.data
            user_data['tokens'] = tokens  # Add tokens to the response data
            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    Authenticates a user and returns JWT tokens.
    """
    
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
            
            tokens = get_tokens_for_user(user)
            user_data = UserCreateSerializer(user).data
            user_data['tokens'] = tokens
            return Response(user_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    """
    Logs out a user by blacklisting their refresh token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        print("refresh_token", refresh_token)   
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response({"success": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid or already blacklisted token"}, status=status.HTTP_400_BAD_REQUEST)

class Hello(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return Response({"hello": "heloo world"})





key = Fernet.generate_key()  # use Fernet.generate_key()
cipher = Fernet(key)

def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data):
    return cipher.decrypt(data.encode()).decode()

@method_decorator(ratelimit(key='user', rate='5/m', block=True), name='dispatch')
class PredictSentimentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        text = request.data.get('text', '')
        platform = request.data.get('platform', '')

        if not text or not platform:
            return Response({'error': 'No input text or platform provided'}, status=status.HTTP_400_BAD_REQUEST)

        sentiment = predict_sentiment(text, platform)
        # encrypt_result = encrypt_data(sentiment)

        return Response({'result': sentiment}, status=status.HTTP_200_OK)
