from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.views import APIView

from caki_app.models import Like,Keep,Member,Post
from caki_app.serializers import *
from caki_app.APIView.get_others import *
from mysite.settings import MAIN_DOMAIN
import requests

class KeepPost(APIView):
    def get(self,request):
        access_token = request.headers.get('Authorization').split(' ')[1]
        response = requests.get (
                f"{MAIN_DOMAIN}/authuser/userview/",
                headers={"Authorization": f"Bearer {access_token}"},
            ).json()
        # 인증 실패
        if response['message'] != 'success':
            return JsonResponse({"message" : "logout"})
        user_info = response['user_info']
        idmember = user_info['idmember']
        nickname = user_info['nickname']

        keep_instances = Keep.objects.filter(member_idmember=idmember).order_by('-date').distinct()
        post_list = []
        for keep_instance in keep_instances:
            post_instance = keep_instance.post_idpost
            pull_posts = {
                # "post_writer" : get_post_writer(post_instance),
                # "post_body" : model_to_dict(post_instance),
                # "post_theme" : get_post_theme(post_instance),
                # "post_like" : get_post_like(post_instance,idmember)
                "post_id" : post_instance.idpost,
                "post_view" : None,
                "post_title" : post_instance.title,
                "post_like" : get_post_like(post_instance,idmember),
                "post_keep" : get_post_keep(post_instance,idmember),
            }
            post_list.append(pull_posts)

        res = JsonResponse({
            "user_info" : {
                "idmember" : idmember,
                "nickname" : nickname,
            },
            "post_list" : post_list,
            "message" : 'success'
            })

        return res
            
    

class LikePost(APIView):  
    def get (self,request,idpost,idmember):
        # 좌표가 없으면 서울을 기준
        nx = int(self.request.GET.get('nx','55'))
        ny = int(self.request.GET.get('ny','127'))

        member_instance = get_object_or_404(Member,pk= idmember)
        post_instance = get_object_or_404(Post,pk= idpost)
        like_instance = Like.objects.create(
            member_idmember = member_instance,
            post_idpost = post_instance,
            weather = get_weather(nx,ny)
        )
        res = JsonResponse({
            "like_info" : get_post_like(idpost,idmember),
            "message" : 'success'
            })
        return res
    
    def delete (self,request,idpost,idmember):
        Like.objects.filter(
            post_idpost=idpost, 
            member_idmember=idmember
            ).delete()
        
        res = JsonResponse({
            "like_info" : get_post_like(idpost,idmember),
            "message" : 'success'
            })
        return res



class AddKeep(APIView):
    def get (self,request,idpost,idmember):
        member_instance = get_object_or_404(Member,pk= idmember)
        post_instance = get_object_or_404(Post,pk= idpost)
        keep = Keep.objects.create(
            member_idmember = member_instance,
            post_idpost = post_instance
        )
        res = JsonResponse({
            "keep_info" : get_post_keep(idpost,idmember),
            "message" : 'success'
            })
        return res
    
    # keep 삭제
    def delete (self,request,idpost,idmember):
        Keep.objects.filter(
            post_idpost=idpost, 
            member_idmember=idmember
            ).delete()
        
        res = JsonResponse({
            "keep_info" : get_post_keep(idpost,idmember),
            "message" : 'success'
            })
        return res