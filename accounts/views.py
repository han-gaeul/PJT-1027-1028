from django.shortcuts import redirect, render
from .forms import CustomChangeForm, CustomCreationForm, ProfileForm
from .models import Profile
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

# Create your views here.

# 회원 가입
def signup(request):
    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        profile = Profile()
        if form.is_valid():
            user = form.save()
            profile.user = user
            profile.save()
            auth_login(request, user)
            return redirect('reviews:index')
    else:
        form = CustomCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/signup.html', context)

# 로그인
def login(request):
    if request.user.is_authenticated:
        return redirect('reviews:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'reviews:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/login.html', context)

# 로그아웃
def logout(request):
    auth_logout(request)
    return redirect('reviews:index')

# 비밀번호 변경
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form
    }
    return render(request, 'accounts/change_password.html', context)

# 회원 정보
def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        'user' : user
    }
    return render(request, 'accounts/detail.html', context)

# 회원 정보 수정
def update(request):
    if request.method == 'POST':
        form = CustomChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = CustomChangeForm(instance=request.user)
    context = {
        'form' : form
    }
    return render(request, 'accounts/update.html', context)

# 내 프로필
def profile(request):
    user = request.user
    reviews = user.review_set.all()
    comments = user.comment_set.all()
    profile = user.profile_set.all()
    context = {
        'reviews' : reviews,
        'comments' : comments,
        'profile' : profile,
    }
    return render(request, 'accounts/profile.html', context)

# 프로필 수정
@login_required
def profile_update(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    current_user = user.profile_ser.all()[0]
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=current_user)
    context = {
        'form' :form
    }
    return render(request, 'accounts/profile_update.html', context)