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



# 저장된 게시글
class KeepPost(APIView):
    def get(self,request):
        access_token = request.headers.get('Authorization').split(' ')[1]
        user_info = access_token_authentication(access_token)
        
        idmember = user_info['idmember']
        nickname = user_info['nickname']

        keep_instances = Keep.objects.filter(member_idmember=idmember).order_by('-date').distinct()
        post_list = []
        for keep_instance in keep_instances:
            post_instance = keep_instance.post_idpost
            pull_posts = get_post_preview(post_instance)
            post_list.append(pull_posts)

        res = JsonResponse({
            "user_info" : user_info,
            "post_list" : post_list,
            "message" : 'success'
            })

        return res
            
    
# 게시글 좋아요/ 취소
class LikePost(APIView):  
    def get (self,request,idpost):
        access_token = request.headers.get('Authorization').split(' ')[1]
        user_info = access_token_authentication(access_token)

        idmember = user_info['idmember']
        # 좌표가 없으면 서울을 기준
        nx = int(self.request.GET.get('nx','55'))
        ny = int(self.request.GET.get('ny','127'))

        member_instance = get_object_or_404(Member,pk= idmember)
        post_instance = get_object_or_404(Post,pk= idpost)
        if Like.objects.filter(post_idpost=idpost,member_idmember = idmember).exists():
            Like.objects.get(post_idpost=idpost, member_idmember = idmember).delete()
        else:
            Like.objects.create(
                member_idmember = member_instance,
                post_idpost = post_instance,
                weather = get_weather(nx,ny)
            )
        res = JsonResponse({
            "like_info" : get_post_like(idpost,idmember),
            "message" : 'success'
            })
        return res
    


# 게시글 저장/ 취소
class AddKeep(APIView):
    def get (self,request,idpost):
        access_token = request.headers.get('Authorization').split(' ')[1]
        user_info = access_token_authentication(access_token)
        idmember = user_info['idmember']
        member_instance = get_object_or_404(Member,pk= idmember)
        post_instance = get_object_or_404(Post,pk= idpost)

        if Keep.objects.filter(post_idpost=idpost,member_idmember = idmember).exists():
            Keep.objects.get(post_idpost=idpost, member_idmember = idmember).delete()
        else:
            Keep.objects.create(
                member_idmember = member_instance,
                post_idpost = post_instance
            )
        res = JsonResponse({
            "keep_info" : get_post_keep(idpost,idmember),
            "message" : 'success'
            })
        return res
    
