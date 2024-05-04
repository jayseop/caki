from django.shortcuts import get_object_or_404,redirect
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.views import APIView

from caki_app.models import Post,Member,Temp,Theme
from caki_app.serializers import *

from mysite.settings import MAIN_DOMAIN
import requests
import datetime



# 게시글 작성 api
# {
#     "contents" :{
#                     "title": "독도",
#                     "view" : "test_view",
#                     "text" : "만드는 방법",
#                     "idmember" : 13
#                 },
#     "keyword":  {
#                     "술종류" : ["보드카","진"],
#                     "당도" : ["당도1"],
#                     "도수" : ["도수1"],
#                     "음료" : []
#                 }
# }

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
        

    def create_post(self,post_title,post_view,post_text,idmember):
        member_instance = get_object_or_404(Member,pk = idmember)

        new_post = Post.objects.create(
            title = post_title,
            view = post_view,
            text = post_text,
            date = datetime.datetime.now(),
            member_idmember = member_instance
        )
        # 생성된 게시글의 기본키
        return new_post 
    

    def create_theme(self,new_post,keywords):
        for value in keywords:
            theme_instance = get_object_or_404(Theme,state = value)    
            temp_instance = Temp.objects.create(
                theme_idtheme = theme_instance,
                post_idpost = new_post
            )

        return temp_instance

    def post(self,request,nickname):
        # 내용 저장
        contents = request.data['post_body']
        new_post = self.create_post(
            post_title = contents['title'],
            post_view = contents['view'],
            post_text = contents['text'],
            idmember = contents['idmember'])

        # 키워드 저장
        keywords = request.data['post_theme']
        self.create_theme( 
            new_post, 
            keywords
        )


        res = JsonResponse({
            "new_post": model_to_dict(new_post),
            "message" : 'success'
            })

        return res