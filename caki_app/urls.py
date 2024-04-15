from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'caki_app'

urlpatterns = [
    # path('', main_page, name='main'), #메인 페이지 url
    path("signup/", SignupAPIView.as_view(), name='signup'), # post - 회원가입
    path('authuser/', AuthUserAPIView.as_view(), name='authuser'), # 
    path("authsuer/refresh/", TokenRefreshView.as_view()), # jwt 토큰 재발급
]