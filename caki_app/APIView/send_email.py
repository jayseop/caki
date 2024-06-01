from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from rest_framework.views import APIView
from caki_app.models import  *
from django.http import JsonResponse
from mysite.settings import *
import random
import string


def send_email(request, to_email,code):
    # 이메일 본문 텍스트
    message = (
        f"안녕하세요.\n\n"
        f"CAKI_APP에 오신 것을 환영합니다! 아래 코드를 입력하여 EMAIL을 활성화하세요:\n\n"
        f"{code}\n\n"
        "만약 이 메일을 요청하지 않으셨다면, 이 메일을 무시하셔도 됩니다.\n\n"
        "감사합니다,\n"
        "CAKI_APP 팀"
    )

    # 이메일 전송
    email = EmailMessage(
        subject='[CAKI_APP] EMAIL 인증을 완료해주세요.',
        body=render_to_string('email_verification.html', {'code': code}),
        to=[to_email],
        from_email = NAVER_EMAIL
    )
    email.content_subtype = 'html'  # HTML 컨텐츠 설정
    return email.send(fail_silently=False)



class EmailVerification(APIView):
    def post (self,request):
        email = request.data.get("email")
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        send_email(request,email,code)
        res = JsonResponse({
            "code" : code,
            "messege" : "success"
        })
        return res

