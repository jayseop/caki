from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.views import APIView

from caki_app.models import Like,Keep,Member,Post
from caki_app.serializers import *
from caki_app.APIView.get_others import *
from mysite.settings import MAIN_DOMAIN
import requests


class Profile(APIView):
    def get(self,request,profile_nick):
        access_token = request.headers.get('Authorization').split(' ')[1]
        response = requests.get (
                f"{MAIN_DOMAIN}/authuser/userview/",
                headers={"Authorization": f"Bearer {access_token}"},
            ).json()
    
        user_info = response['user_info']
    
        
        profile_instance = get_object_or_404(Member,nickname = profile_nick)

        post_instances = Post.objects.filter(member_idmember=profile_instance).order_by('-date')
        post_list = []
        for post_instance in post_instances:
            pull_posts = {
                # "post_writer" : get_post_writer(post_instance),
                # "post_body" : model_to_dict(post_instance),
                # "post_theme" : get_post_theme(post_instance),
                # "post_like" : get_post_like(post_instance,idmember)
                "post_id" : post_instance.idpost,
                "post_view" : post_instance.view,
                "post_title" : post_instance.title,
                "post_like" : get_post_like(post_instance,profile_instance),
                "post_keep" : get_post_keep(post_instance,profile_instance),
            }
            post_list.append(pull_posts)
        res = JsonResponse({
            "profile_info" : {
                "idmember" :  profile_instance.idmember,
                "nickname" : profile_nick,
                "introduce" : profile_instance.introduce,
                "image_url" : get_member_image(profile_instance),
                },
            "my_info" : True if user_info['idmember'] is profile_instance.pk else False,
            "post_list" : post_list,
            "message" : 'success',
            })

        return res