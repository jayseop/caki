from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Q

from rest_framework.views import APIView

from caki_app.models import Like,Keep,Member,Post
from caki_app.serializers import *
from caki_app.APIView.get_others import *
from caki_app.APIView.user_api_views import access_token_authentication

from mysite.settings import MAIN_DOMAIN
import requests
import json
from datetime import datetime, timedelta
from pprint import pprint
from django.utils import timezone



class Main(APIView):
    def get_post_by_ranking(self,idmember):
        # 태그별 점수 부여
        tag_score={}
        score_ratio = 1
        idpost_list = Postviews.objects.filter(member_idmember = idmember).values_list('post_idpost', flat=True)
        for idpost in idpost_list:
            tag_list = Tag.objects.filter(post_idpost = idpost).values_list('tag', flat=True)
            for tag in tag_list:
                if tag in tag_score:
                    tag_score[tag] += score_ratio
                else:
                    tag_score[tag] = score_ratio


        # 예외 처리
        query = Q() #쿼리 객체 생성
        # 내 게시글 예외
        query &= Q(member_idmember__in = str(idmember))
        
        # 저장된 게시글 예외
        keep_idpost = Keep.objects.filter(member_idmember = idmember).values_list('post_idpost', flat=True)
        query &= Q(idpost__in = keep_idpost)
        



        # 점수 매기기
        post_score={}
        idpost_100_list = Post.objects.exclude(query).order_by('-date').values_list('idpost', flat=True)[:100]
        for idpost in idpost_100_list:
            post_score[idpost] = 0 # 점수 초키화

            # 본 게시글의 태그별 점수
            tag_list = Tag.objects.filter(post_idpost = idpost).values_list('tag', flat=True)
            for tag in tag_list:
                if idpost in post_score:
                    post_score[idpost] += tag_score.get(tag, 0)
            
            # 저장한 게시글 유저가 쓴 다른 게시글 
            keep_idpost_list = Keep.objects.filter(member_idmember = idmember).values_list('post_idpost', flat=True)
            
            # 7일 전 날짜 계산
            current_date = timezone.now()
            seven_days_ago = current_date - timedelta(days=7)

            for idpost in keep_idpost_list:
                post_idmember = Post.objects.get(pk = idpost).member_idmember.pk
                recent_idpost_list = Post.objects.filter(member_idmember = post_idmember,date__gte=seven_days_ago).values_list('idpost', flat=True)
                
                for idpost in recent_idpost_list:
                    if idpost in post_score:
                        post_score[idpost] += 1/8
            


        # 점수 높은 순으로 정렬
        sorted_items = sorted(post_score.items(), key=lambda x: (x[1], x[0]), reverse=True)
        top_items = sorted_items[:10]

        post_list = []
        for top_post in top_items:
            idpost = top_post[0] # ex) top_post = (idpost, score), ...
            post_instance = get_object_or_404(Post,pk = idpost)
            post_preview = get_post_preview(post_instance)
            post_list.append(post_preview)
        post_by_ranking = {
            "post_by_ranking" : post_list
        }

        return post_by_ranking



    def get_post_by_like(self,idmember):
        current_date = timezone.now()
        # current_date = datetime.strptime(timezone.get_current_timezone(), '%B %d, %Y')
        # 7일 전 날짜 계산
        seven_days_ago = current_date - timedelta(days=7)
        # 좋아요 테이블을 조회하고, 최근 7일 동안의 데이터만 필터링
        recent_likes = Like.objects.filter(date__gte=seven_days_ago)
        # 게시글 별로 좋아요 수를 집계
        liked_posts = recent_likes.values('post_idpost').annotate(like_count=Count('post_idpost'))
        # 게시글 좋아요 순으로 가져오기
        top_post_instances = liked_posts.order_by('-like_count')[:10]

        # idpost = top_post['post_idPost']로 post 인스턴스 생성
        post_list = []
        for top_post in top_post_instances:
            idpost = top_post['post_idpost']
            post_instance = get_object_or_404(Post,pk = idpost)
            post_preview = get_post_preview(post_instance)
            post_list.append(post_preview)

        post_by_like = {
            "post_by_like" : post_list
        }
        return post_by_like
    
    def get_post_by_weather(self,idmember,nx,ny):
        weather = get_weather(nx,ny)
        like_by_weather = Like.objects.filter(weather = weather)

        liked_posts = like_by_weather.values('post_idpost').annotate(like_count=Count('post_idpost'))
        # 게시글 좋아요 순으로 가져오기
        top_post_instances = liked_posts.order_by('-like_count')[:10]

        # idpost = top_post['post_idPost']로 post 인스턴스 생성
        post_list = []
        for top_post in top_post_instances:
            idpost = top_post['post_idpost']
            post_instance = get_object_or_404(Post,pk = idpost)
            post_preview = get_post_preview(post_instance)
            post_list.append(post_preview)

        post_by_weather = {
            "post_by_weather" : post_list
        }
        return post_by_weather

    def get(self,request):
        access_token = request.headers.get('Authorization').split(' ')[1]
        user_info = access_token_authentication(access_token)
        idmember = user_info['idmember']
        nickname = user_info['nickname']

        weekly_trends = []
        weekly_trends.append(self.get_post_by_like(idmember)) # 좋아요 많이 받은 순
       
        # 현재 날씨에 좋아요 많이 받은 순
        # 좌표가 없으면 서울을 기준
        nx = int(self.request.GET.get('nx','55'))
        ny = int(self.request.GET.get('ny','127'))
        weekly_trends.append(self.get_post_by_weather(idmember,nx,ny)) 

        weekly_trends.append(self.get_post_by_ranking(idmember))
        res = JsonResponse({
            "user_info" : user_info,
            "weekly_trends" : weekly_trends,
        })
        return res
    
class AlcoholCategory(APIView):
    def get(self, request, category):
        access_token = request.headers.get('Authorization').split(' ')[1]
        user_info = access_token_authentication(access_token)
        idmember = user_info['idmember']
        post_list = []

        post_instances = Post.objects.all().order_by()
        for post_instance in post_instances:
            if Tag.objects.filter(post_idpost = post_instance.pk, tag = category).exists():
                post_preview = get_post_preview(post_instance)
                post_list.append(post_preview)

        res = JsonResponse({
                    "user_info" : user_info,
                    "post_list" : post_list,
                    "message" : 'success'
                    })

        return res
