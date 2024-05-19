from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.views import APIView

from caki_app.models import Like,Keep,Member,Post
from caki_app.serializers import *
from caki_app.APIView.get_others import *
from caki_app.APIView.user_api_views import access_token_authentication
from mysite.settings import MAIN_DOMAIN
import requests


class Profile(APIView):
    def get(self,request,profile_nick):
        try:
            access_token = request.headers.get('Authorization').split(' ')[1]
            user_info = access_token_authentication(access_token)
        except Exception as e:
            return{"message" : str(e)}
        idmember = user_info["idmember"]
        
        profile_instance = get_object_or_404(Member,nickname = profile_nick)

        post_instances = Post.objects.filter(member_idmember=profile_instance).order_by('-date')
        post_list = []
        for post_instance in post_instances:
            post_preview = get_post_preview(post_instance)
            post_list.append(post_preview)

        res = JsonResponse({
            "user_info" : idmember,
            "profile_info" : {
                "idmember" :  profile_instance.idmember,
                "nickname" : profile_nick,
                "introduce" : profile_instance.introduce,
                "image_url" : get_member_image(profile_instance.idmember),
                },
            "post_list" : post_list,
            "message" : 'success',
            })

        return res