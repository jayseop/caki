from django.urls import path
from .APIView.user_api_views import *
from .APIView.social_login_view import *
from .APIView.create_post_view import *
from .APIView.like_post_view import *
from.APIView.search_post_view import *
from .APIView.change_myinfo_view import *

from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'caki_app'

urlpatterns = [
    # 회원가입 - post
    path("signup/", SignupAPIView.as_view(), name='signup'),    
    # 로그인 - post, 로그아웃 - delete
    path('authuser/', AuthUserAPIView.as_view(), name='authuser'),

    # 유저 인증
    path("authuser/userview/",UserView.as_view(),name = 'userview'),
    
    #소셜 로그인
    path('authuser/naver/login', NaverLoginAPIView.as_view()),
    path('authuser/naver/callback', NaverCallbackAPIView.as_view()),
    path('authuser/google/login', GoogleLoginAPIView.as_view()),
    path('authuser/google/callback', GoogleCallbackAPIView.as_view()),

    # 게시글 생성
    path('createpost/<str:nickname>/',CreatePost.as_view(),name = 'createpost'),
    # 게시글 좋아요 확인 - get, 좋아요 - post, 삭제 - delete
    path('like/<int:idpost>/<int:idmember>/',LikePost.as_view(),name = 'likepost'),
    # 저장된 게시글 - get, 저장 - post, 삭제 - delete
    path('keep/<int:idpost>/<int:idmember>/',KeepPost.as_view(),name = 'keeppost'),
    # 게시글 검색
    path('search/',SearchPost.as_view(), name = 'searchpost'),

    # 마이페이지
    path('myinfo/', ChangeInfo.as_view(), name='info'),
]