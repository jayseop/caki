from django.http import JsonResponse
from django.db.models import Q
from django.forms.models import model_to_dict

from rest_framework.views import APIView

from caki_app.models import Post
from caki_app.APIView.get_others import *
from mysite.settings import MAIN_DOMAIN

import requests
import re

class SearchView(APIView):
    def get(self,request):
        title_list = list(Post.objects.values_list('title', flat=True))
        res = JsonResponse({
            "title_list" : title_list,
        })
        return res
    
class Search(APIView):
    def split_text(self,search_text):
        kor = re.compile("[가-힣]+").findall(search_text) 
        eng = re.compile("[a-zA-Z]+").findall(search_text)
        num = re.compile("[0-9]+").findall(search_text)
        temp_search_text = kor + eng + num

        # ex) 아이폰se2 -> ["아이폰","se","2"]
        return temp_search_text
    
    def get_post_list(sellf,search_terms,keywords,idmember):

        query = Q() #쿼리 객체 생성
        for term in search_terms: #분할한 단어로 조건문 생성
            query |= Q(title__icontains = term)| Q(text__icontains = term) #제목과 본문 필터링
        post_instances = Post.objects.filter(query).order_by('-date').distinct() #distinct() -> 중복값 제거
        
        post_list=[]
        for post_instance in post_instances:
            # 게시글의 테마 가져옴
            post_theme = get_post_theme(post_instance)

            #keyword가 post_theme의 부분집합일때
            if set(keywords).issubset(set(post_theme)) or keywords == [''] :
                pull_posts = {
                    # "post_writer" : get_post_writer(post_instance),
                    # "post_body" : model_to_dict(post_instance),
                    # "post_theme" : post_theme,
                    "idpsot" : post_instance.idpost,
                    "post_view" : post_instance.view,
                    "post_title": post_instance.title,
                    "post_like" : get_post_like(post_instance,idmember),
                    "post_keep" : get_post_keep(post_instance,idmember),
                }
                post_list.append(pull_posts)

        return post_list


    def get(self,request):
        cookies = request.COOKIES
        response = requests.get (
                f"{MAIN_DOMAIN}/authuser/userview/"
                ,cookies=cookies # 쿠키도 함께 전달
            ).json()
        # 인증 실패
        if response['message'] != 'success':
            return JsonResponse({"message" : "logout"})
        user_info = response['user_info']
        idmember = user_info['idmember']        


        search = self.request.GET.get('q','')
        keywords = self.request.GET.get("k",'').split(',')

        search_terms = self.split_text(search) # 한글, 영어, 숫자로 검색어 분할
        post_list = self.get_post_list(search_terms,keywords,idmember)

        res = JsonResponse({
            "search": search_terms,
            "keywords" : keywords,
            "post_list":post_list,
        })
        return res
    