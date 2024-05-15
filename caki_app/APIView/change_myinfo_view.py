from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from caki_app.models import Member
from caki_app.APIView.get_others import *
from mysite.settings import MAIN_DOMAIN
import requests

class ChangeInfo(APIView):
    def get(self, request):
        try:
            access_token = request.headers.get('Authorization').split(' ')[1]
            response = requests.get (
                    f"{MAIN_DOMAIN}/authuser/userview/",
                    headers={"Authorization": f"Bearer {access_token}"},
                ).json()
            # 인증 실패
            if response['message'] != 'success':
                return JsonResponse({"message" : "logout"})
            
            # 사용자 인증이 되었을 경우
            user_info = response['user_info']
            idmember = user_info['idmember']

            res = JsonResponse({
                "user_info" :user_info,
                "image" : get_member_image(idmember)
            })

            return res

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        try:
            access_token = request.headers.get('Authorization').split(' ')[1]
            response = requests.get (
                    f"{MAIN_DOMAIN}/authuser/userview/",
                    headers={"Authorization": f"Bearer {access_token}"},
                ).json()
            # 인증 실패
            if response['message'] != 'success':
                return JsonResponse({"message" : "logout"})
            
            # 사용자 인증이 되었을 경우
            user_info = response['user_info']
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
                user_image = get_object_or_404(MemberImage,member_idmember = idmember)
                new_image = request.FILES['image']
                user_image.image_path = new_image
                user_image.save()

            return JsonResponse({
                'user_info' : user_info,
                'image_url' : user_image.image_path.url,
                'message': 'success',
            }, status=status.HTTP_200_OK)
                    
               
        except Exception as e:
            return JsonResponse({
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChangeDefultImage(APIView):
    def get(self, request, idmember):
        if idmember is None:
            return JsonResponse({"message" : "idmember is none"})
        MemberImage.objects.filter(pk = idmember ).delete()
        return JsonResponse({"image_url" : get_member_image(idmember)})