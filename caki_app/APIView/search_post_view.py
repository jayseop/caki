from django.http import JsonResponse
from django.db.models import Q
from django.forms.models import model_to_dict

from rest_framework.views import APIView

from caki_app.models import Post
from caki_app.APIView.get_post_others import get_post_theme

import re


class SearchPost(APIView):
    def split_text(self,search_text):
        kor = re.compile("[가-힣]+").findall(search_text) 
        eng = re.compile("[a-zA-Z]+").findall(search_text)
        num = re.compile("[0-9]+").findall(search_text)
        temp_search_text = kor + eng + num

        # ex) 아이폰se2 -> ["아이폰","se","2"]
        return temp_search_text
    
    def get_post_list(sellf,search_terms,keywords):

        query = Q()
        for term in search_terms:
            query |= Q(title__icontains = term)| Q(text__icontains = term)
        posts = Post.objects.filter(query).distinct()
        post_list=[]
        for post in posts:
            post_theme = get_post_theme(post)
            #keyword가 post_theme의 부분집합일때
            if set(keywords).issubset(set(post_theme)) or keywords == [''] :
                post_body = model_to_dict(post)
                pull_posts = {
                    "post_body" : post_body,
                    "post_theme" : post_theme,
                }

            post_list.append(pull_posts)
        return post_list


    def get(self,request):
        search = self.request.GET.get('q','')
        keywords = self.request.GET.get("k",'').split(',')

        search_terms = self.split_text(search) # 한글, 영어, 숫자로 검색어 분할
        post_list = self.get_post_list(search_terms,keywords)

        res = JsonResponse({
            "search": search_terms,
            "post_list":post_list,
        })
        return res
    