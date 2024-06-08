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
        nickname = user_info['nickname']
        user = get_object_or_404(Member,pk=idmember)
        
        # 닉네임 변경
        new_nickname = request.data.get('nickname',None)
        if  new_nickname:
            existing_user = Member.objects.filter(nickname=new_nickname).exists()
            if existing_user:
                return JsonResponse({
                    'message': 'nickname already exist',
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.nickname = new_nickname


        # 이메일 변경
        new_email = request.data.get('email',None)
        if  new_email:
            existing_user = Member.objects.filter(email=new_email).exists()
            if existing_user:
                return JsonResponse({
                    'message': 'email already exist',
                }, status=status.HTTP_400_BAD_REQUEST)
            user.email = new_email


        # 비밀번호 변경
        new_password = request.data.get('password',None)
        if  new_password:
            user.set_password(new_password)
 
            
        # 자기소개 변경
        new_introduce =request.data.get('introduce',None)
        if new_introduce:
            new_introduce = request.data['introduce']
            user.introduce = new_introduce


        # 사진 변경
        new_image = request.FILES.get('image',None)
        
        if new_image:
            if user.image_path: #기존 사진 삭제
               user.delete_image()
            user.image_path = new_image
        
        user.save()

        token = LoginSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        return JsonResponse({
            "user_info" : {
                "idmember" :  user.idmember,
                "nickname" : user.nickname,
                "introduce" : user.introduce,
                "qual" : user.qual,
                "image_url" : get_member_image(user.idmember),
                },
            "access_token" : access_token,
            "refresh_token" : refresh_token,
            'message': 'success',
        }, status=status.HTTP_200_OK)

                    
class DefultImage(APIView):   
    def get(self, request):
        access_token = request.headers.get('Authorization').split(' ')[1]
        user_info = access_token_authentication(access_token)
        # 사용자 인증이 되었을 경우
        idmember = user_info['idmember']
        member_instance = Member.objects.get(pk = idmember)
        if member_instance.image_path == '':
            return JsonResponse({"message" : "profile image is defult"})
        member_instance.delete_image()
        return JsonResponse({'message': 'success'})