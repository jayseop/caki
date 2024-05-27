from django.urls import path
from .APIView.user_api_views import *
from .APIView.social_login_view import *
from .APIView.post_view import *
from .APIView.keep_like_view import *
from .APIView.search_view import *
from .APIView.main_view import *
from .APIView.profile_view import *
from .APIView.review_api_view import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'caki_app'

urlpatterns = [
    # 회원가입 - post
    path("signup/", SignupAPIView.as_view(), name='signup'),    
    # 로그인 - post, 로그아웃 - delete
    path('authuser/', AuthUserAPIView.as_view(), name='authuser'),

    # access token 재발급
    path("token/refresh/",TokenRefreshView.as_view(), name='token_refresh'),
     
    #소셜 로그인
    path('authuser/naver/login/', NaverLoginAPIView.as_view()),
    path('authuser/naver/callback', NaverCallbackAPIView.as_view()),
    path('authuser/google/login/', GoogleLoginAPIView.as_view()),
    path('authuser/google/callback', GoogleCallbackAPIView.as_view()),

    # 메인뷰
    path('main/',Main.as_view(),name="main"),
    # 카테고리별 뷰
    path('main/<str:category>/',AlcoholCategory.as_view(),name = 'alcoholcategory'),

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
    path('keep/<int:idpost>/',AddKeep.as_view(),name='addkeep'),
    # 게시글 좋아요 확인 - get, 좋아요 - post, 삭제 - delete
    path('like/<int:idpost>/',LikePost.as_view(),name = 'likepost'),
    # 키워드 리뷰
    path('review/<int:idpost>/',KeywordReview.as_view(),name = 'review'),

    # 검색 페이지
    path('searchview/',SearchView.as_view(),name="searchview"),
    # 검색
    path('search/',Search.as_view(), name = 'searchpost'),

    # 프로필 뷰 - get, 수정 - put 
    path('<str:profile_nick>/',Profile.as_view(), name = 'profile'),
    # 프로필 기본 사진 변경
    path('defult_image/',DefultImage.as_view(), name= 'defultimage'),
] 
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    # 업로드 된 URL, 실제 파일 위치