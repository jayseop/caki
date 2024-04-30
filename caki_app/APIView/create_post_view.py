from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404,redirect
from django.http import JsonResponse

from rest_framework import status
from rest_framework.views import APIView

from caki_app.models import Post,Member
from caki_app.serializers import *

from mysite.settings import MAIN_DOMAIN

import requests



class CreatePost (APIView):
    def get(self,request,nickname):
        try: # 유저 인증
            cookies = request.COOKIES
            response = requests.get (
                    f"{MAIN_DOMAIN}/authuser/userview/"
                    ,cookies=cookies # 쿠키도 함께 전달
                )
            response_json = response.json()
            # 인증 성공
            if response_json['user_info']['nickname'] == nickname:
                return JsonResponse(response_json) # 게시글 작성 화면
            
        except: #인증 실패
            return JsonResponse({ #로그인 뷰
                "message": "error",
            }, status=status.HTTP_404_NOT_FOUND)
        
    def post(self,request,nickname):

        post_title = request.data['title']
        post_view = request.data['view']
        post_text = request.data['text']
        idmember = request.data['idmember']
        member_instance = get_object_or_404(Member,pk= idmember)
        res = Post.objects.create(
            title = post_title,
            view = post_view,
            text = post_text,
            member_idmember = member_instance
        )
        #태그는 미완성
        return JsonResponse({"message" : res})