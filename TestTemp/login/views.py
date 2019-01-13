import hashlib
import json

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

from login import forms
from login import models
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', locals())

def regist(request):
    return render(request, 'regist.html', locals())
def task(request):
    return render(request, 'task.html', locals())

def gen_md5(s, salt='login'):  #加盐
    s += salt
    md5 = hashlib.md5()
    md5.update(s.encode(encoding='utf-8')) # update方法只接收bytes类型
    return md5.hexdigest()

def login(request):
        if request.session.get('is_login', None):
            messages.warning(request, "请勿重复登录！")
            return redirect("/index/")

        if request.method == "POST":
            login_form = forms.LoginForm(request.POST)
            if not login_form.is_valid():
                render(request, 'login.html', locals())

            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            if models.Admin.objects.filter(name=username).exists():
                group = 'admin'
                admin = models.Admin.objects.get(name=username)
                if admin.password != gen_md5(password, username):
                    messages.error(request, "密码错误！")
                    return render(request, 'login.html', locals())
            elif models.User.objects.filter(name=username).exists():
                group = 'user'
                user = models.User.objects.get(name=username)
                if user.password != gen_md5(password, username):
                    messages.error(request, "密码错误！")
                    return render(request, 'login.html', locals())
            else:
                messages.error(request, "用户名未注册！")
                return render(request, 'login.html', locals())

            request.session['is_login'] = True
            request.session['group'] = group
            request.session['username'] = username
            messages.success(request, "登录成功！")
            request.session.set_expiry(3600)
            return redirect('/task/')

        login_form = forms.LoginForm()
        return render(request, 'login.html', locals())

def regist(request):
    if request.session.get('is_login', None):
        messages.warning(request, "请先退出后再注册！")
        return redirect("/index/")

    if request.method == "POST":
        if 'login' in request.POST:
            return redirect("/login/")
        register_form = forms.RegisterForm(request.POST)
        if not register_form.is_valid():
            messages.error(request, "表单信息有误！")
            return render(request, 'regist.html', locals())

        username = register_form.cleaned_data['username']
        password1 = register_form.cleaned_data['password1']
        password2 = register_form.cleaned_data['password2']
        email = register_form.cleaned_data['email']
       # phone = register_form.cleaned_data['phone']
      #  sex = register_form.cleaned_data['sex']

        if password1 != password2:  # 两次密码是否相同
            messages.error(request, "两次输入的密码不一致！")
            return render(request, 'regist.html', locals())
        if models.Admin.objects.filter(name=username).exists() or \
                models.User.objects.filter(name=username).exists():  # 用户名是否唯一
            messages.error(request, "该用户名已注册！")
            return render(request, 'regist.html', locals())
        if models.Admin.objects.filter(email=email).exists() or \
                models.User.objects.filter(email=email).exists():  # 邮箱地址是否唯一
            messages.error(request, "该邮箱已注册！")
            return render(request, 'regist.html', locals())
    #if models.Admin.objects.filter(phone=phone).exists() or \
        #        models.User.objects.filter(phone=phone).exists():  # 手机号是否唯一
         #   messages.error(request, "该手机号已注册！")
         #   return render(request, 'login/register.html', locals())

        new_user = models.User.objects.create()
        new_user.name = username
        new_user.password = gen_md5(password1, username)
        new_user.email = email
    #    new_user.phone = phone
     #   new_user.sex = sex
        new_user.save()

        messages.success(request, "注册成功！")
        return redirect('/login/')

    register_form = forms.RegisterForm()
    return render(request, 'regist.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        messages.warning(request, "您尚未登录！")
        return redirect("/index/")

    request.session.flush()
    messages.success(request, "退出成功！")
    return redirect("/index/")