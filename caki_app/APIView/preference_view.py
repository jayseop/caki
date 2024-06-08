from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from caki_app.models import *
from caki_app.serializers import *
from caki_app.APIView.get_others import *
from caki_app.APIView.user_api_views import access_token_authentication

class InsertPreference(APIView):
    def post(self,request):
        access_token = request.headers.get('Authorization').split(' ')[1]
        user_info = access_token_authentication(access_token)

        idmember = user_info["idmember"]

        new_preference = request.data.get('preference',None)
        if new_preference:
            Preference.objects.create(
                member_idmember = Member.objects.get(pk = idmember),
                preference = ", ".join(new_preference),
            )

        res = JsonResponse({  
            'message' : 'success' 
        })
        
        return res