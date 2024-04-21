from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404,redirect
from rest_framework import status
from django.http import JsonResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.views import APIView
from caki_app.models import Member
from caki_app.serializers import *
from mysite.settings import SECRET_KEY
import jwt



# access token으로 유저 식별
class UserView(APIView) :
  def get(self,request): 
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access_token = request.COOKIES.get('access',None)
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256']) # access 토큰으로 유저 확인
            pk = payload.get('user_id') # pk = idMember
            user = get_object_or_404(Member, pk=pk) # 데이터 베이스에서 유저 정보 추출
            serializer = UserSerializer(instance=user)
            res = JsonResponse({
                    'user' : serializer.data,
                    'message': 'success',
                    },status=status.HTTP_200_OK)
            return res
        
        # access 토큰 만료 시 토큰 갱신
        except(jwt.exceptions.ExpiredSignatureError):
            data = {'refresh': request.COOKIES.get('refresh', None)} # refrash 토큰 추출
            serializer = TokenRefreshSerializer(data=data) # refrash 토큰으로 access토큰 발급
            if serializer.is_valid(raise_exception=True): 
                access_token = serializer.validated_data.get('access', None) # access 토큰 추출
                # refresh_token = serializer.validated_data.get('refresh', None) # refrash 토큰 재발급

                payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256']) # access 토큰으로 유저 확인
                pk = payload.get('user_id') # pk = idMember
                user = get_object_or_404(Member, pk=pk) # 데이터 베이스에서 유저 정보 추출

                serializer = UserSerializer(instance=user)
                res = JsonResponse({
                    'user' : serializer.data,
                    'message': 'success',
                    },status=status.HTTP_200_OK)
                
                res.set_cookie('access', access_token) 
                # res.set_cookie('refresh', refresh_token)
                return res
            raise jwt.exceptions.InvalidTokenError

        # refrash 토큰 만료 및 로그아웃 유저
        except(jwt.exceptions.InvalidTokenError):
            return JsonResponse({"message": "none",}) # 로그인 페이지


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
        return JsonResponse('signup_page') # 회원가입 페이지
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() 
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = JsonResponse(
                {
                    "user": serializer.data,
                    'message': 'success',
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res #회원가입 성공시 페이지
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# 로그인
class AuthUserAPIView(APIView):
    def get(self, request):        
        return JsonResponse('login_page') #로그인 페이지

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
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = JsonResponse(
                {
                    "user": serializer.data,
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
    