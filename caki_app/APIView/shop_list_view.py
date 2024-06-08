from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from caki_app.models import  *
from django.http import JsonResponse
from mysite.settings import *
from rest_framework.views import APIView
from caki_app.APIView.user_api_views import access_token_authentication
from mysite.settings import BASE_DIR


class ShopList(APIView):
    def get(self,request):
        # access_token = request.headers.get('Authorization').split(' ')[1]
        # user_info = access_token_authentication(access_token)
        # idmember = user_info['idmember']
        shop_list = os.path.join(BASE_DIR,'caki_app','shop_list.json')

        # JSON 파일 읽기
        with open(shop_list, 'r',encoding='utf-8') as file:
            res = JsonResponse({
                "shop_list":json.load(file)
                })

        return res
