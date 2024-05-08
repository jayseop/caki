from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.views import APIView

from caki_app.models import  *
from caki_app.APIView.get_others import *
from mysite.settings import MAIN_DOMAIN
import requests



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

class PostView(APIView):
    def get(self,request,idpost):
        cookies = request.COOKIES
        response = requests.get (
                f"{MAIN_DOMAIN}/authuser/userview/"
                ,cookies=cookies # 쿠키도 함께 전달
            ).json()
        
        #인증 실패
        if response['message'] != "success":
            return JsonResponse({ #로그인 뷰
                "message": "logout",
            }, status=status.HTTP_404_NOT_FOUND)
        
        user_info = response['user_info']
        idmember = user_info['idmember']

        post_instance = get_object_or_404(Post,pk = idpost)
        res = JsonResponse({
            "user_info" : {
                'idmember' : user_info['idmember'],
                'nickname' : user_info['nickname'],
            },
            "post_writer" : get_post_writer(post_instance),
            "post_body" : model_to_dict(post_instance),
            "post_theme" : get_post_theme(post_instance),
            "post_like" : get_post_like(post_instance,idmember)
        })
        return res # 게시글 뷰
        



class CreatePost (APIView):
    def get(self,request):
        cookies = request.COOKIES
        response = requests.get (
                f"{MAIN_DOMAIN}/authuser/userview/"
                ,cookies=cookies # 쿠키도 함께 전달
            ).json()
        #인증 실패
        if response['message'] != "success":
            return JsonResponse({ #로그인 뷰
                "message": "logout",
            }, status=status.HTTP_404_NOT_FOUND)
        user_info = response['user_info'] 

        res = {
            "user_info" :{
                'idmember' : user_info['idmember'],
                'nickname' : user_info['nickname'],
            }
        }
        return JsonResponse(res) # 게시글 작성 화면
        

    def create_post(self,post_title,post_view,post_text,idmember):
        member_instance = get_object_or_404(Member,pk = idmember)

        new_post = Post.objects.create(
            title = post_title,
            view = post_view,
            text = post_text,
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

    def post(self,request):
        # 내용 저장
        post_body = request.data['post_body']
        new_post = self.create_post(
            post_title = post_body['title'],
            post_view = post_body['view'],
            post_text = post_body['text'],
            idmember = post_body['idmember'])

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
    

# 마이 페이지에서 유저 인증을 하였으니 
# 따로 유저 인증은 필요 없어보임
class DeletePost(APIView):
    def delete(self,request,idpost):
        try:
            Keep.objects.filter(post_idpost = idpost).delete()
            Like.objects.filter(post_idpost = idpost).delete()
            Temp.objects.filter(post_idpost = idpost).delete()
            Image.objects.filter(post_idpost = idpost).delete()
            Video.objects.filter(post_idpost = idpost).delete()

            Post.objects.filter(idpost = idpost).delete()


            return JsonResponse({'message':'success'})
        except:
            return JsonResponse({'message' : 'empty idpost'})


class EditPost(APIView):
    def get(self,request,idpost):
        cookies = request.COOKIES
        response = requests.get (
                f"{MAIN_DOMAIN}/authuser/userview/"
                ,cookies=cookies # 쿠키도 함께 전달
            ).json()
        #인증 실패
        if response['message'] != "success":
            return JsonResponse({ #로그인 뷰
                "message": "logout",
            }, status=status.HTTP_404_NOT_FOUND)
        
        user_info = response['user_info']
        
        post_instance = get_object_or_404(Post,pk = idpost)
        res = JsonResponse({
            "user_info" : {
                'idmember' : user_info['idmember'],
                'nickname' : user_info['nickname'],
            },
            "post_body" : model_to_dict(post_instance),
            "post_theme" : get_post_theme(post_instance),             
            "message" : "success",
        })
        
        # 인증 성공
        return res # 작성된 게시글  


    def edit_post(self,post_body,idpost):
        post_instance = get_object_or_404(Post,pk = idpost)


        post_instance.title = post_body['title']
        post_instance.view = post_body['view']
        post_instance.text = post_body['text']

        post_instance.date = timezone.localtime(timezone.now())
        post_instance.save()
        # 생성된 게시글의 기본키
        return post_instance 
    

    def edit_theme(self,edit_post,keywords):
        Temp.objects.filter(post_idpost = edit_post).delete()
        for value in keywords:
            theme_instance = get_object_or_404(Theme,state = value)    
            temp_instance = Temp.objects.create(
                theme_idtheme = theme_instance,
                post_idpost = edit_post
            )

        return temp_instance
        

    def put(self,request,idpost):
        cookies = request.COOKIES
        response = requests.get (
                f"{MAIN_DOMAIN}/authuser/userview/"
                ,cookies=cookies # 쿠키도 함께 전달
            ).json()
        #인증 실패
        if response['message'] != "success":
            return JsonResponse({ #로그인 뷰
                "message": "logout",
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 내용 수정
        post_body = request.data['post_body']       
        edit_post = self.edit_post(
            post_body = post_body,
            idpost = idpost
            )

        # 키워드 수정
        keywords = request.data['post_theme']
        self.edit_theme( 
            edit_post=edit_post, 
            keywords=keywords
        )
        res = JsonResponse({
            "edit_post": model_to_dict(edit_post),
            "message" : 'success'
            })

        return res