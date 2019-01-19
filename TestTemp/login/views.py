import hashlib
import json

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.datastructures import MultiValueDict
from login import forms
from login import models
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', locals())

def regist(request):
    if request.session.get('is_login', None):
        messages.warning(request, "请先退出后再注册！")
        return redirect("/index/")

    if request.method == "POST":
        if 'login' in  request.POST:
            return redirect("/login/")
        register_form = forms.RegisterForm(request.POST)
        if not register_form.is_valid():
            messages.error(request, "表单信息有误！")
            return render(request, 'regist.html', locals())

        username = register_form.cleaned_data['username']
        password1 = register_form.cleaned_data['password1']
        password2 = register_form.cleaned_data['password2']
        email = register_form.cleaned_data['email']

        if password1 != password2:  # 两次密码是否相同
            messages.error(request, "两次输入的密码不一致！")
            return render(request, 'regist.html', locals())
        if models.User.objects.filter(name=username).exists():  # 用户名是否唯一
            messages.error(request, "该用户名已注册！")
            return render(request, 'regist.html', locals())
        if models.User.objects.filter(email=email).exists():  # 邮箱地址是否唯一
            messages.error(request, "该邮箱已注册！")
            return render(request, 'regist.html', locals())

        new_user = models.User.objects.create()
        new_user.name = username
        new_user.password = gen_md5(password1, username)
        new_user.email = email
        new_user.is_admin = False  # 只能注册普通用户
        new_user.save()
        print(new_user.c_time)
        messages.success(request, "注册成功！")
        return redirect('/login/')

    register_form = forms.RegisterForm()
    return render(request, 'regist.html', locals())


def release_task(request):
    #if not request.session.get('is_admin', None):
     #   messages.warning(request, "您没有权限查看该页面！")
     #   return redirect("/index/")
    request.session['new_task_id'] = None
    if request.method == "POST":

        if 'template' in request.POST:
            if request.session.get('new_task_id', None):
                new_task = models.Task.objects.get(id=request.session['new_task_id'])
            else:
                new_task = models.Task.objects.create()
                new_task.admin = models.User.objects.get(name=request.session['username'])
                new_task.save()
                request.session['new_task_id'] = new_task.id
            if request.POST.get('template') == '1':
                new_task.template = 1
                new_task.save()
                return redirect("/release_task/")
            elif request.POST.get('template') == '2':
                new_task.template = 2
                new_task.save()
                return redirect("/release_task/")
            elif request.POST.get('template') == '3':
                new_task.template = 3
                new_task.save()
                return redirect("/release_task/")
        if 'task_name' in request.POST:
            task_form3 = forms.TaskForm3(request.POST)
            if not task_form3.is_valid():
                messages.error(request, "表单信息有误！")
                return render(request, 'release_task.html', locals())
    task_form1 = forms.TaskForm1()
    task_form2 = forms.TaskForm2()
    task_form3 = forms.TaskForm3()
    return render(request, 'release_task.html', locals())

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



def logout(request):
    if not request.session.get('is_login', None):
        messages.warning(request, "您尚未登录！")
        return redirect("/index/")

    request.session.flush()
    messages.success(request, "退出成功！")
    return redirect("/index/")