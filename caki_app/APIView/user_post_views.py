from django.http import JsonResponse
from rest_framework import status
from caki_app.serializers import PostSerializer
from .user_api_views import UserView
from caki_app.models import Post

class CheckLoginAPIView(UserView):
    def get(self, request):
        response = super().get(request)
        # 로그인이 확인되면 사용자 정보를 반환
        return response

class CreatePost(CheckLoginAPIView):
    def get(self, request):
        return JsonResponse('post_page')
    
    def post(self, request):
        try:
            # 게시글 작성에 필요한 로직을 구현합니다.
            # 이 부분에는 게시글을 생성하고 저장하는 코드가 들어갑니다.
            return JsonResponse({"message": "Post created successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
