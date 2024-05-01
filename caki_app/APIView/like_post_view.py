from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.core.serializers import serialize
from rest_framework.views import APIView

from caki_app.models import Like,Keep,Member,Post
from caki_app.serializers import *
from caki_app.APIView.get_post_others import get_post_theme

class LikePost(APIView):

    def get(self,request,idpost,idmember):
        like_exists = Like.objects.filter(post_idpost = idpost,member_idmember = idmember).exists()
        like_cnt = Like.objects.filter(post_idpost = idpost).count()
        res = JsonResponse({
            "like_cnt" : like_cnt,
            "like_exists": True if like_exists else False
        })
        return res
    
    def post (self,request,idpost,idmember):
        member_instance = get_object_or_404(Member,pk= idmember)
        post_instance = get_object_or_404(Post,pk= idpost)
        Like.objects.create(
            member_idmember = member_instance,
            post_idpost = post_instance
        )
        return JsonResponse({"message" : 'success'})
    
    def delete (self,request,idpost,idmember):
        Like.objects.filter(
            post_idpost=idpost, 
            member_idmember=idmember
            ).delete()
        return JsonResponse({"message" : 'success'})


class KeepPost(APIView):
    def get(self,request,idpost,idmember):
        keep_instances = Keep.objects.filter(member_idmember=idmember).distinct()
        post_list = []

        for keep_instance in keep_instances:
            post_instance = keep_instance.post_idpost

            post_body = model_to_dict(post_instance)
            post_theme = get_post_theme(post_instance)

            pull_posts = {
                    "post_body" : post_body,
                    "post_theme" : post_theme,
                }
            post_list.append(pull_posts)

        res = JsonResponse({
            "post_list" : post_list,
            "message" : 'success'
            })

        return res
    
    def post (self,request,idpost,idmember):
        member_instance = get_object_or_404(Member,pk= idmember)
        post_instance = get_object_or_404(Post,pk= idpost)
        keep = Keep.objects.create(
            member_idmember = member_instance,
            post_idpost = post_instance
        )
        res = JsonResponse({
            "keep" : model_to_dict(keep),
            "message" : 'success'})
        return res
    
    def delete (self,request,idpost,idmember):
        Keep.objects.filter(
            post_idpost=idpost, 
            member_idmember=idmember
            ).delete()
        
        res = JsonResponse({"message" : 'success'})
        return res