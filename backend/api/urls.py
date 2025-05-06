from django.urls import path
from . import views

urlpatterns = [
    path('csrf/', views.CSRFTokenView.as_view(), name='csrf'),
    path('send_otp', views.SendOTPView.as_view()),
    path('verify_otp', views.VerifyOTPView.as_view()),
    path('sign_up', views.SignupView.as_view()),
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('hello', views.Hello.as_view()),
    path('predict', views.PredictSentimentView.as_view()),
]