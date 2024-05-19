from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from caki_app.models import Member
from caki_app.APIView.get_others import *
from caki_app.APIView.user_api_views import access_token_authentication
from mysite.settings import MAIN_DOMAIN
from django.conf import settings
import requests
import os

class ChangeInfo(APIView):
    def get(self, request):
        try:
            access_token = request.headers.get('Authorization').split(' ')[1]
            user_info = access_token_authentication(access_token)
            
            # 사용자 인증이 되었을 경우
            idmember = user_info['idmember']
            res = JsonResponse({
                "user_info" :user_info,
                "message" : "success",
            })

            return res

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        try:
            access_token = request.headers.get('Authorization').split(' ')[1]
            user_info = access_token_authentication(access_token)
        except Exception as e:
            return{"message" : str(e)}
            
        # 사용자 인증이 되었을 경우
        idmember = user_info['idmember']
        
        user = get_object_or_404(Member,pk=idmember)
        
        # 닉네임 변경
        if 'nickname' in request.data:
            new_nickname = request.data['nickname']
            existing_user = Member.objects.filter(nickname=new_nickname).exists()

            if existing_user:
                return JsonResponse({
                    'message': 'nickname already exist',
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.nickname = new_nickname
            user.save()

        # 비밀번호 변경
        if 'password' in request.data:
            new_password = request.data['password']
            user.set_password(new_password)
            user.save()
            
        # 자기소개 변경
        if 'introduce' in request.data:
            new_introduce = request.data['introduce']
            user.introduce = new_introduce
            user.save()
        
        # 사진 변경
        if 'image' in request.FILES:
            if get_member_image(user.idmember): #기존 사진 삭제
                image_file_path = os.path.join(settings.MEDIA_ROOT, user.image_path.name)
                os.remove(image_file_path)# 이미지 삭제

            new_image = request.FILES['image']
            user.image_path = new_image
            user.save()

        return JsonResponse({
            "m" : user.image_path.url,
            'message': 'success',
        }, status=status.HTTP_200_OK)
                    
class ChangeDefultImage(APIView):
    def get(self, request, idmember):
        if idmember is None:
            return JsonResponse({"message" : "idmember is none"})
        member_instance = get_object_or_404(Member,pk = idmember)

        image_file_path = os.path.join(settings.MEDIA_ROOT, member_instance.image_path.name)
        curr_dir_path = os.path.dirname(image_file_path)
        if os.path.isfile(image_file_path): # 이미지 삭제
            os.remove(image_file_path)
        if os.path.exists(curr_dir_path): # 이미지 상위 폴더 삭제
            os.rmdir(curr_dir_path)
        
        member_instance.image_path = None
        member_instance.save()
        res = JsonResponse({
            "image_url" : get_member_image(idmember)
        })
        return res