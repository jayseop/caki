from django.urls import path
from .APIView.user_api_views import *
from .APIView.social_login_view import *
from .APIView.create_post_view import *
from .APIView.like_post_view import *
from .APIView.change_myinfo_view import *

from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'caki_app'

urlpatterns = [
    # path('', main_page, name='main'), #메인 페이지 url
    path("signup/", SignupAPIView.as_view(), name='signup'), # post - 회원가입
    path('authuser/', AuthUserAPIView.as_view(), name='authuser'), # post - 로그인, delete - 로그아웃
    # path("authuser/refresh/", TokenRefreshView.as_view()), # jwt 토큰 재발급
    # path("test/onlyuserview/",OnlyUserView.as_view(),name = 'onlyuserview')
    path("authuser/userview/",UserView.as_view(),name = 'userview'), #토큰 확인
    
    #소셜 로그인
    path('authuser/naver/login', NaverLoginAPIView.as_view()),
    path('authuser/naver/callback', NaverCallbackAPIView.as_view()),
    path('authuser/google/login', GoogleLoginAPIView.as_view()),
    path('authuser/google/callback', GoogleCallbackAPIView.as_view()),

    # 게시글 생성
    path('<str:nickname>/createpost/',CreatePost.as_view(),name = 'createpost'),

    # 게시글 좋아요
    path('like/<int:idpost>/<int:idmember>/',LikePost.as_view(),name = 'likepost'),

    # 마이페이지
    path('myinfo/', ChangeInfo.as_view(), name='info')
]