from django.http import JsonResponse
from django.db.models import Q
from django.forms.models import model_to_dict

from rest_framework.views import APIView

from caki_app.models import Post
from caki_app.APIView.get_others import *
from caki_app.APIView.user_api_views import access_token_authentication
from mysite.settings import MAIN_DOMAIN

import requests
import re

class SearchView(APIView):
    def get(self,request):
        access_token = request.headers.get('Authorization').split(' ')[1]
        user_info = access_token_authentication(access_token)
        title_list = list(Post.objects.values_list('title', flat=True))
        res = JsonResponse({
            "user_info" : user_info,
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
            post_tag = get_post_tag(post_instance)

            #keyword가 post_theme의 부분집합일때
            if set(keywords).issubset(set(post_tag)) or keywords == [''] :
                post_preview = get_post_preview(post_instance)
                post_list.append(post_preview)

        return post_list


    def get(self,request):
        access_token = request.headers.get('Authorization').split(' ')[1]
        user_info = access_token_authentication(access_token)

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
    