from django.urls import path
from .APIView.user_api_views import *
from .APIView.social_login_view import *
from .APIView.post_view import *
from .APIView.keep_post_view import *
from .APIView.search_view import *
from .APIView.main_view import *
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
    path('authuser/naver/login/', NaverLoginAPIView.as_view()),
    path('authuser/naver/callback', NaverCallbackAPIView.as_view()),
    path('authuser/google/login/', GoogleLoginAPIView.as_view()),
    path('authuser/google/callback', GoogleCallbackAPIView.as_view()),

    # 메인뷰
    path('main/',Main.as_view(),name="main"),

    # 게시글 보기
    path('postview/<int:idpost>/',PostView.as_view(),name='postview'),
    # 게시글 생성
    path('createpost/',CreatePost.as_view(),name = 'createpost'),
    # 저장된 게시글 - get, 저장 - post, 삭제 - delete
    path('keeppost/',KeepPost.as_view(),name = 'keeppost'),
    #게시글 삭제 get - 삭제
    path('deletepost/<int:idpost>/',DeletePost.as_view(), name='deletepsot'),
    # 게시글 수정 post - 수정
    path('editpost/<int:idpost>/',EditPost.as_view(),name='editpsot'),
    # 게시글 저장 - get, 삭제 -delete
    path('addkeep/<int:idpost>/<int:idmember>/',AddKeep.as_view(),name='addkeep'),
    # 게시글 좋아요 확인 - get, 좋아요 - post, 삭제 - delete
    path('like/<int:idpost>/<int:idmember>/',LikePost.as_view(),name = 'likepost'),
    # 검색 페이지
    path('searchview/',SearchView.as_view(),name="searchview"),
    # 검색
    path('search/',Search.as_view(), name = 'searchpost'),

    # 마이페이지
    path('myinfo/', ChangeInfo.as_view(), name='info'),
]