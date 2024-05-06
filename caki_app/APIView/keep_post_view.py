from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.views import APIView

from caki_app.models import Like,Keep,Member,Post
from caki_app.serializers import *
from caki_app.APIView.get_post_others import *
from mysite.settings import MAIN_DOMAIN
import requests

class KeepPost(APIView):
    def get(self,request):
        cookies = request.COOKIES
        user_info = requests.get (
                f"{MAIN_DOMAIN}/authuser/userview/"
                ,cookies=cookies # 쿠키도 함께 전달
            ).json()
        # 인증 실패
        if user_info['message'] != 'success':
            return JsonResponse({"message" : "logout"})
        
        idmember = user_info['user_info']['idmember']
        nickname = user_info['user_info']['nickname']

        keep_instances = Keep.objects.filter(member_idmember=idmember).order_by('-date').distinct()
        post_list = []
        for keep_instance in keep_instances:
            post_instance = keep_instance.post_idpost
            pull_posts = {
                "post_writer" : get_post_writer(post_instance),
                "post_body" : model_to_dict(post_instance),
                "post_theme" : get_post_theme(post_instance),
                "post_like" : get_post_like(post_instance,idmember)
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
        member_instance = get_object_or_404(Member,pk= idmember)
        post_instance = get_object_or_404(Post,pk= idpost)
        like_instance = Like.objects.create(
            member_idmember = member_instance,
            post_idpost = post_instance,
        )
        return JsonResponse({
            "add_like" : model_to_dict(like_instance),
            "message" : 'success'})
    
    def delete (self,request,idpost,idmember):
        Like.objects.filter(
            post_idpost=idpost, 
            member_idmember=idmember
            ).delete()
        return JsonResponse({"message" : 'success'})



class AddKeep(APIView):
    def get (self,request,idpost,idmember):
        member_instance = get_object_or_404(Member,pk= idmember)
        post_instance = get_object_or_404(Post,pk= idpost)
        keep = Keep.objects.create(
            member_idmember = member_instance,
            post_idpost = post_instance
        )
        res = JsonResponse({
            "add_keep" : model_to_dict(keep),
            "message" : 'success'})
        return res
    
    def delete (self,request,idpost,idmember):
        Keep.objects.filter(
            post_idpost=idpost, 
            member_idmember=idmember
            ).delete()
        
        res = JsonResponse({"message" : 'success'})
        return res