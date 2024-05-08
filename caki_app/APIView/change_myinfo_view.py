from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from caki_app.models import Member
from caki_app.serializers import UserSerializer
from mysite.settings import MAIN_DOMAIN
import requests

class ChangeInfo(APIView):
    def get(self, request):
        try:
            # 사용자 인증
            cookies = request.COOKIES
            response = requests.get(
                f"{MAIN_DOMAIN}/authuser/userview/",
                cookies=cookies  # 요청과 함께 쿠키 전송
            )
            response_json = response.json()
            
          # 사용자 인증이 되었을 경우
            if 'user_info' in response_json:
                return redirect('/myinfo/')

            else:
                # 로그인되어 있지 않으면 로그인 페이지로 리다이렉트
                return JsonResponse('signup_page')
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        try:
            # 사용자 인증
            cookies = request.COOKIES
            response = requests.get(
                f"{MAIN_DOMAIN}/authuser/userview/",
                cookies=cookies  # 요청과 함께 쿠키 전송
            )
            response_json = response.json()
            
            # 사용자 인증이 되었을 경우
            if 'user_info' in response_json:
                user_id = response_json['user_info']['id']
                user = Member.objects.get(pk=user_id)
                
                # 닉네임 변경
                if 'nickname' in request.data:
                    new_nickname = request.data['nickname']
                    existing_user = Member.objects.filter(nickname=new_nickname).exclude(id=user_id)
                    if not existing_user:
                        user.nickname = new_nickname
                        user.save()
                        return JsonResponse({
                            'message': '닉네임이 성공적으로 변경되었습니다.',
                        }, status=status.HTTP_200_OK)
                    else:
                        return JsonResponse({
                            'message': '이미 사용 중인 닉네임입니다.',
                        }, status=status.HTTP_400_BAD_REQUEST)
                
                # 비밀번호 변경
                if 'password' in request.data:
                    new_password = request.data['password']
                    user.set_password(new_password)
                    user.save()
                    return JsonResponse({
                        'message': '비밀번호가 성공적으로 변경되었습니다.',
                    }, status=status.HTTP_200_OK)
                
                # 자기소개 변경
                if 'introduce' in request.data:
                    new_introduce = request.data['introduce']
                    user.introduce = new_introduce
                    user.save()
                    return JsonResponse({
                        'message': '자기소개가 성공적으로 변경되었습니다.',
                    }, status=status.HTTP_200_OK)
                
                return JsonResponse({
                    'message': '변경할 내용을 입력하세요 (닉네임, 비밀번호, 자기소개).',
                }, status=status.HTTP_400_BAD_REQUEST)
                    
            else:
                return JsonResponse({
                    'message': '사용자 인증에 실패했습니다.',
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except Exception as e:
            return JsonResponse({
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)