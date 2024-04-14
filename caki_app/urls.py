from django.contrib import admin
from django.urls import path
from .import views

app_name = 'myapp'

urlpatterns = [
    path('',views.main_page, name='main'), #메인 페이지 url
    path('login/', views.user_login, name='login'), # 일단 로그인 url, 메인 url로 설정 추후 변경 예정
    path('signup/', views.user_signup, name='signup') # 회원가입 페이지 url 
]