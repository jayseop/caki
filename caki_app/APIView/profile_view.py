from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from caki_app.models import Like,Keep,Member,Post
from caki_app.serializers import *
from caki_app.APIView.get_others import *
from caki_app.APIView.user_api_views import access_token_authentication
from mysite.settings import MAIN_DOMAIN
import requests


class Profile(APIView):
    def get(self,request,profile_nick):
        access_token = request.headers.get('Authorization').split(' ')[1]
        user_info = access_token_authentication(access_token)

        idmember = user_info["idmember"]
        
        profile_instance = get_object_or_404(Member,nickname = profile_nick)

        post_instances = Post.objects.filter(member_idmember=profile_instance).order_by('-date')
        post_list = []
        for post_instance in post_instances:
            post_preview = get_post_preview(post_instance)
            post_list.append(post_preview)

        res = JsonResponse({
            "user_info" : user_info,
            "profile_info" : {
                "idmember" :  profile_instance.idmember,
                "nickname" : profile_nick,
                "introduce" : profile_instance.introduce,
                "qual" : profile_instance.qual,
                "image_url" : get_member_image(profile_instance.idmember),
                },
            "post_list" : post_list,
            "message" : 'success',
            })

        return res
    
    # 프로필 수정
    def put(self, request, profile_nick):
        access_token = request.headers.get('Authorization').split(' ')[1]
        user_info = access_token_authentication(access_token)

            
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
            'user_info' : user_info,
            'message': 'success',
        }, status=status.HTTP_200_OK)

                    
class DefultImage(APIView):
    def get(self, request):

        access_token = request.headers.get('Authorization').split(' ')[1]
        user_info = access_token_authentication(access_token)
            
        # 사용자 인증이 되었을 경우
        idmember = user_info['idmember']
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
            "image_url" : get_member_image(idmember),
            'message': 'success',
        })
        return res