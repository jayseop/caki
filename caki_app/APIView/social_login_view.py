
from django.http import JsonResponse
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import requests

from caki_app.models import Member
from mysite.settings import *

# from allauth.socialaccount.providers.naver import views as naver_views
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView

# main domain(http://127.0.0.1:8000)
main_domain = MAIN_DOMAIN


# DRF의 APIView를 상속받아 View를 구성
class NaverLoginAPIView(APIView):    
    def get(self, request, *args, **kwargs):
        client_id = NAVER_CLIENT_ID
        response_type = "code"
        # Naver에서 설정했던 callback url을 입력
        uri = main_domain + "/authuser/naver/callback"
        state = 'naver_login'
        # Naver Document 에서 확인했던 요청 url
        url = "https://nid.naver.com/oauth2.0/authorize"
        
        # Document에 나와있는 요소들을 담아서 요청한다.
        res = redirect(
            f'{url}?response_type={response_type}&client_id={client_id}&redirect_uri={uri}&state={state}'
        )
        print(res)
        return JsonResponse({"M" : res})



class NaverCallbackAPIView(APIView):   
    def get(self, request, *args, **kwargs):
        try:
            # Naver Login Parameters
            grant_type = 'authorization_code'
            client_id = NAVER_CLIENT_ID
            client_secret = NAVER_CLIENT_SECRET
            code = request.GET.get('code')
            state = request.GET.get('state')

            parameters = f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}"

            # token request
            token_request = requests.get(
                f"https://nid.naver.com/oauth2.0/token?{parameters}"
            )

            token_response_json = token_request.json()
            access_token = token_response_json.get("access_token")

            # User info get request
            user_info_request = requests.get(
                "https://openapi.naver.com/v1/nid/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            # User 정보를 가지고 오는 요청이 잘못된 경우
            if user_info_request.status_code != 200:
                return JsonResponse({"error": "failed to get email."}, status=status.HTTP_400_BAD_REQUEST)

            user_info = user_info_request.json().get("response")
            email = user_info["email"]
            nickname = user_info["nickname"]

            # User 의 email 을 받아오지 못한 경우
            if email is None:
                return JsonResponse({
                    "error": "Can't Get Email Information"
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = Member.objects.get(email=email)
                data = {'email': email,
                        'password' : email+nickname}
                accept = requests.post(
                    f"{main_domain}/authuser/", json=data
                )
                if accept.status_code != 200:
                    return JsonResponse({"error": "Failed to Signin."}, status=accept.status_code)
                return JsonResponse(accept.json(), status=status.HTTP_200_OK)

            except Member.DoesNotExist:
                data = {'email': email,
                        'password' : email+nickname,
                        'nickname': nickname}
                accept = requests.post(
                    f"{main_domain}/signup/", json=data
                )
                # token 발급
                return JsonResponse(accept.json(), status=status.HTTP_200_OK)
                
        except:
            return JsonResponse({
                "message": "error",
            }, status=status.HTTP_404_NOT_FOUND)

class GoogleLoginAPIView(APIView):    
    def get(self, request, *args, **kwargs):
        client_id = GOOGLE_CLIENT_ID
        response_type = "code"
        # callback url을 입력
        uri = main_domain + "/authuser/google/callback"
        scope = "email profile"
        url = "https://accounts.google.com/o/oauth2/v2/auth"
        return redirect(
            f'{url}?response_type={response_type}&client_id={client_id}&redirect_uri={uri}&scope={scope}'
        )


class GoogleCallbackAPIView(APIView):   
    def get(self, request, *args, **kwargs):
        # try:
            # Google Login Parameters
            client_id = GOOGLE_CLIENT_ID
            client_secret = GOOGEL_CLIENT_SECRET
            code = request.GET.get('code')
            grant_type = 'authorization_code'
            uri = main_domain + "/authuser/google/callback/"
            state = 'google_login'

            parameters = f"client_id={client_id}&client_secret={client_secret}&code={code}&grant_type={grant_type}&redirect_uri={uri}&state={state}"

            # token request
            token_request = requests.post(
                f"https://oauth2.googleapis.com/token?{parameters}"
            )
            
            token_response_json = token_request.json()            
            access_token = token_response_json.get("access_token")
            # User info get request
            user_info_request = requests.get(
                f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")

            # User 정보를 가지고 오는 요청이 잘못된 경우
            if user_info_request.status_code != 200:
                return JsonResponse({"error": "failed to get email."}, status=status.HTTP_400_BAD_REQUEST)

            user_info = user_info_request.json()
            print(user_info)
            email = user_info["email"]
            nickname = user_info["user_id"]

            # User 의 email 을 받아오지 못한 경우
            if email is None:
                return JsonResponse({
                    "error": "Can't Get Email Information"
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = Member.objects.get(email=email)
                data = {'email': email,
                        'password' : email+nickname}
                accept = requests.post(
                    f"{main_domain}/authuser/", json=data
                )
                if accept.status_code != 200:
                    return JsonResponse({"error": "Failed to Signin."}, status=accept.status_code)
                return JsonResponse(accept.json(), status=status.HTTP_200_OK)

            except Member.DoesNotExist:
                data = {'email': email,
                        'password' : email+nickname,
                        'nickname': nickname}
                accept = requests.post(
                    f"{main_domain}/signup/", json=data
                )
                # token 발급
                return JsonResponse(accept.json(), status=status.HTTP_200_OK)
                
        # except:
        #     return JsonResponse({
        #         "message": "error",
        #     }, status=status.HTTP_404_NOT_FOUND)