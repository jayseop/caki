from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import Count

from rest_framework.views import APIView

from caki_app.models import Like,Keep,Member,Post
from caki_app.serializers import *
from caki_app.APIView.get_others import *

from mysite.settings import MAIN_DOMAIN
import requests
import json
from datetime import datetime, timedelta

def get_pull_post(post_instance):
    post = {
        # "post_writer" : get_post_writer(post_instance),
        # "post_body" : model_to_dict(post_instance),
        # "post_theme" : get_post_theme(post_instance),
        "post_id" : post_instance.pk,
        "post_view" : None,
        "post_title" : post_instance.title,
        # "post_like" : get_post_like(post_instance,idmember),
        # "post_keep" : get_post_keep(post_instance,idmember),
        }
    return post


class Main(APIView):
    def get_post_by_like(self,idmember):
        current_date = timezone.localtime(timezone.now())
        # 7일 전 날짜 계산
        seven_days_ago = current_date - timedelta(days=7)
        # 좋아요 테이블을 조회하고, 최근 7일 동안의 데이터만 필터링
        recent_likes = Like.objects.filter(date__gte=seven_days_ago)
        # 게시글 별로 좋아요 수를 집계
        liked_posts = recent_likes.values('post_idpost').annotate(like_count=Count('post_idpost'))
        # 게시글 좋아요 순으로 가져오기
        top_post_instances = liked_posts.order_by('-like_count')

        # idpost = top_post['post_idPost']로 post 인스턴스 생성
        post_list = []
        for top_post in top_post_instances:
            idpost = top_post['post_idpost']
            post_instance = get_object_or_404(Post,pk = idpost)
            pull_post = get_pull_post(post_instance)
            post_list.append(pull_post)

        post_by_like = {
            "post_by_like" : post_list
        }
        return post_by_like
    
    def get_post_by_weather(self,idmember,nx,ny):
        weather = get_weather(nx,ny)
        like_by_weather = Like.objects.filter(weather = weather)

        liked_posts = like_by_weather.values('post_idpost').annotate(like_count=Count('post_idpost'))
        # 게시글 좋아요 순으로 가져오기
        top_post_instances = liked_posts.order_by('-like_count')

        # idpost = top_post['post_idPost']로 post 인스턴스 생성
        post_list = []
        for top_post in top_post_instances:
            idpost = top_post['post_idpost']
            post_instance = get_object_or_404(Post,pk = idpost)
            pull_post = get_pull_post(post_instance)
            post_list.append(pull_post)

        post_by_weather = {
            "post_by_weather" : post_list
        }
        return post_by_weather

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

        weekly_trends = []
        weekly_trends.append(self.get_post_by_like(idmember)) # 좋아요 많이 받은 순
       
        # 현재 날씨에 좋아요 많이 받은 순
        # 좌표가 없으면 서울을 기준
        nx = int(self.request.GET.get('nx','55'))
        ny = int(self.request.GET.get('ny','127'))
        weekly_trends.append(self.get_post_by_weather(idmember,nx,ny)) 

        res = JsonResponse({
            "user_info" : {
                "idmember" : idmember,
                "nickname" : nickname,
            },
            "weekly_trends" : weekly_trends,
        })
        return res