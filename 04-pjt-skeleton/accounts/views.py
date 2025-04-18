from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserUpdateForm, UserLoginForm, UserForm  # 수정된 UserForm 사용
from .models import User

# 로그인
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # 로그인 후 index 페이지로 리다이렉트
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# 로그아웃
def logout_view(request):
    logout(request)  # 세션 종료
    return redirect('login')  # 로그인 페이지로 리다이렉트

# 회원가입
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)  # 수정된 UserForm 사용
        if form.is_valid():
            form.save()  # 새 사용자 저장
            return redirect('index')  # 저장 후 index 페이지로 리다이렉트
    else:
        form = UserForm()
    return render(request, 'accounts/signup.html', {'form': form})

# 회원 정보 수정
def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')  # 수정 후 index 페이지로 리다이렉트
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/update.html', {'form': form})

# 회원 삭제
def delete_profile(request):
    request.user.delete()  # 회원 삭제
    return redirect('index')  # 삭제 후 index 페이지로 리다이렉트

# 비밀번호 변경
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # 로그인 상태 유지
            return redirect('index')  # 변경 후 index로 리다이렉트
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

# 프로필
def profile(request):
    user_profile = request.user
    return render(request, 'accounts/profile.html', {'user_profile': user_profile})

# 팔로우
def follow(request, user_id):
    user_to_follow = User.objects.get(id=user_id)
    if user_to_follow in request.user.followers.all():
        request.user.followers.remove(user_to_follow)  # 팔로우 취소
    else:
        request.user.followers.add(user_to_follow)  # 팔로우 추가
    return redirect('profile')  # 팔로우 후 프로필로 리다이렉트

def index(request):
    return render(request, 'accounts/index.html')
