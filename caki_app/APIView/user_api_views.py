from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404,redirect
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from caki_app.models import *
from caki_app.serializers import *
from caki_app.APIView.get_others import *
from mysite.settings import SECRET_KEY
from pathlib import Path
import jwt


def access_token_authentication(access_token):
    # access token을 decode 해서 유저 id 추출 => 유저 식별
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256']) # access 토큰으로 유저 확인
    user_info = {
        'idmember' : payload.get('user_id'), # pk = idMember
        'nickname' : payload.get('nickname'),
        'email' : payload.get('email'),
        'qual' : payload.get('qual'),
    }
    return user_info

# 회원가입 test용
# {
# 	  "email": "skxcv312@naver.com",
#     "password":"1234",
#     "nickname":"jaja",
#     "qual": "on",
#     "introduce":"hi" 
# }

#회원가입
class SignupAPIView(APIView):
    def get(self, request):
        return JsonResponse({"message":'signup_page'}) # 회원가입 페이지
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() 
            token = LoginSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            res = JsonResponse({
                    "user_info": serializer.data,
                    "access_token" : access_token,
                    "refresh_token" : refresh_token,
                    'message': 'success',
                },
                status=status.HTTP_200_OK,
            )


            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res #회원가입 성공시 페이지

        return JsonResponse(serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)
    


# 로그인
class AuthUserAPIView(APIView):
    def get(self, request):        
        return JsonResponse({'message' : "login_page"}) #로그인 페이지

    # 토큰 발급
    def post(self, request):
    	# 유저 인증
        user = authenticate(
            email=request.data["email"], 
            password=request.data["password"],
        )

        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = LoginSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            idmember = serializer.data['idmember']

            res = JsonResponse(
                {
                    "user_info": serializer.data,
                    "access_token" : access_token,
                    "refresh_token" : refresh_token,
                    'message': 'success',
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return JsonResponse({
                'message' : 'email not available'
            },status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    def delete(self,request):
        # 쿠키에 저장된 토큰 삭제
        res = JsonResponse({
            'message': 'success'
            },status=status.HTTP_202_ACCEPTED)
        
        res.delete_cookie("access")
        res.delete_cookie("refresh")
        return res
    