from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from caki_app.models import Member
import datetime

#회원가입
def user_signup(request):
    if request.method == 'POST': # 정보를 받아옴
        nickname = request.POST['nickname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        date = datetime.datetime.now().date()
        qual = 1 if request.POST.get('qual') else 0 # 전문성이 있으면 1 없으면 0
        introduce = request.POST['introduce']

        # 비밀번호 확인
        if password1 != password2:
            return HttpResponse('Passwords do not match.')
        
        # 이메일 중복 확인.
        if Member.objects.filter(email=email).exists():
            return HttpResponse('Email is already registered. Please use another email address.')
        
        # 닉네임 중복 확인
        if Member.objects.filter(nickname=nickname).exists():
            return HttpResponse('Nickname is already taken. Please choose another one.')


        # 회원 생성 및 데이터베이스에 저장
        user = Member.objects.create(nickname=nickname, 
                                     email=email, 
                                     pwd=password1, 
                                     date = date, 
                                     qual = qual,
                                     introduce = introduce)
        user.save() 


        return redirect('/') # 로그인 페이지
    else:
        # GET 요청일때
        return render(request, 'signup.html') # 회원가입 페이지

# 로그인
def user_login(request):
    if request.method == 'POST':
        # POST 요청일 때 사용자가 입력한 데이터 처리
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 사용자를 데이터베이스에서 찾기
        try:
            user = Member.objects.get(email = email)

        except Member.DoesNotExist:
            # 사용자가 존재하지 않는 경우 에러 메시지 반환
            return HttpResponse("User does not exist")

        # 비밀번호 인증
        if user.pwd == password:
            # 비밀번호가 일치할 경우, 로그인 처리
            #login(request, user) 
            
            #return redirect('/')  # 로그인 성공 시 리다이렉트할 URL
            return HttpResponse("login successful!") # 로그인 성공시 화면

        else:
            # 비밀번호가 일치하지 않을 경우, 에러 메시지 반환
            return HttpResponse("Invalid password")

    else:
        # GET 요청일 때 로그인 폼 보여주기
        return render(request, 'login.html')