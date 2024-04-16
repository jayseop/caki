from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.views import APIView
from caki_app.serializers import *
from mysite.settings import SECRET_KEY

# def main_page(request):
#     return render(request, 'main.html')

#회원가입
class SignupAPIView(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "signup successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return HttpResponse('signup successs') #회원가입 성공시 페이지
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        return render(request,'signup.html')


class AuthUserAPIView(APIView):
    # 유저 정보 확인
    def get(self, request):
        # try:
        #     # access token을 decode 해서 유저 id 추출 => 유저 식별
        #     access = request.COOKIES['access']
        #     payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
        #     pk = payload.get('user_id')
        #     user = get_object_or_404(User, pk=pk)
        #     serializer = UserSerializer(instance=user)
        #     return HttpResponse(serializer.data, status=status.HTTP_200_OK)

        # except(jwt.exceptions.ExpiredSignatureError):
        #     # 토큰 만료 시 토큰 갱신
        #     data = {'refresh': request.COOKIES.get('refresh', None)}
        #     serializer = TokenRefreshSerializer(data=data)
        #     if serializer.is_valid(raise_exception=True):
        #         access = serializer.data.get('access', None)
        #         refresh = serializer.data.get('refresh', None)
        #         payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
        #         pk = payload.get('user_id')
        #         user = get_object_or_404(User, pk=pk)
        #         serializer = UserSerializer(instance=user)
        #         res = Response(serializer.data, status=status.HTTP_200_OK)
        #         res.set_cookie('access', access)
        #         res.set_cookie('refresh', refresh)
        #         return HttpResponse(res)
        #     raise jwt.exceptions.InvalidTokenError

        # except(jwt.exceptions.InvalidTokenError):
        #     # 사용 불가능한 토큰일 때
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
 
        
        return render(request,'login.html')

    # 로그인
    def post(self, request):
    	# 유저 인증
        user = authenticate(
            email=request.data.get("email"), 
            password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return HttpResponse('login successs')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return HttpResponse(response)
