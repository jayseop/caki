from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.core.serializers import serialize
from rest_framework.views import APIView

from caki_app.models import Like,Keep,Member,Post
from caki_app.serializers import *
from caki_app.APIView.get_post_others import *
from mysite.settings import MAIN_DOMAIN
import requests




class MainView(APIView):
    def get(self,request):
        return 0