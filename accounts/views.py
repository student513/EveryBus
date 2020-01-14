from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import SignUpForm,CustomUserChangeForm,ProfileRegisterForm,LoginForm
from django.http import HttpResponse
from django.contrib import auth, messages

def signup(request):
    if request.method == 'POST':
        #signup_form = UserCreationForm(request.POST)
        signup_form = SignUpForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST)
        if signup_form.is_valid() and profile_form.is_valid():
            user = signup_form.save(commit=False)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.info(request,"회원가입이 완료되었습니다.")
            auth.login(request,user)# 회원가입시 자동로그인
            return redirect('home')

    else:
        #signup_form = UserCreationForm()
        signup_form = SignUpForm()
        profile_form = ProfileRegisterForm()
    return render(request, 'accounts/signup.html', {'signup_form':signup_form,'profile_form':profile_form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = auth_authenticate(username = username, password = password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('home')