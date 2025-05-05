from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RegisterForm, LoginForm, ResetPasswordForm
from django.http import HttpResponse
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random, string

# 验证码
def captcha_image(request):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    request.session['captcha'] = code
    img = Image.new('RGB', (100, 40), (255,255,255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 24)
    draw.text((10,5), code, font=font, fill=(0,0,0))
    for _ in range(30):
        x = random.randrange(0,100)
        y = random.randrange(0,40)
        draw.point((x,y), fill=(random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)))
    buf = BytesIO()
    img.save(buf, 'png')
    return HttpResponse(buf.getvalue(), content_type='image/png')

# 首页
def home(request):
    return render(request, 'home.html')

# 注册
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 验证码
            if request.POST.get('captcha', '').upper() != request.session.get('captcha'):
                form.add_error('captcha', '验证码错误')
            else:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.email = form.cleaned_data['email']
                user.save()
                messages.success(request, '注册成功，请登录')
                return redirect('login')
        #   表单或验证码错误
        return render(request, 'users/register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

# 登录
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if request.POST.get('captcha', '').upper() != request.session.get('captcha'):
                form.add_error('captcha', '验证码错误')
            else:
                user = auth.authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
                )
                if user:
                    auth.login(request, user)
                    return redirect('home')
                else:
                    form.add_error(None, '用户名或密码错误')
        return render(request, 'users/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

# 退出
def user_logout(request):
    auth.logout(request)
    return redirect('home')

# 重置密码
def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(username=uname, email=email)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                messages.success(request, '密码已重置，请登录')
                return redirect('login')
            except User.DoesNotExist:
                form.add_error(None, '请检查你的用户名和邮箱')
        return render(request, 'users/reset_password.html', {'form': form})
    else:
        form = ResetPasswordForm()
    return render(request, 'users/reset_password.html', {'form': form})