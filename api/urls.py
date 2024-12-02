from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='analyze'),
    path('analyze', views.sentiment_analysis, name='analyze'),
]