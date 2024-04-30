from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404,redirect
from rest_framework import status
from django.http import JsonResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.views import APIView

from caki_app.models import Like,Member,Post
from caki_app.serializers import *
from caki_app.APIView.user_api_views import UserView
from mysite.settings import SECRET_KEY,MAIN_DOMAIN
import jwt
import requests



class LikePost(APIView):
    def get(self,request,idpost,idmember):
        like_exists = Like.objects.filter(post_idpost = idpost,member_idmember = idmember).exists()
        if like_exists:
            return True # 좋아요 누른 게시물
        else :
            return False
    
    def post (self,request,idpost,idmember):
        member_instance = get_object_or_404(Member,pk= idmember)
        post_instance = get_object_or_404(Post,pk= idpost)
        res = Like.objects.create(
            member_idmember = member_instance,
            post_idpost = post_instance
        )
        return JsonResponse({"message" : res})
    
    def delete (self,request,idpost,idmember):
        res = Like.objects.filter(
            post_idpost=idpost, 
            member_idmember=idmember).delete()
        return JsonResponse({"message" : res})

