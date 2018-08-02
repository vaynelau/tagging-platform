# login/views.py
from django.shortcuts import render, redirect
from login import models
from login import forms


def index(request):
    if not request.session.get('redirect', None):
        request.session['success'] = ""
    request.session['redirect'] = False
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")

    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "表单信息有误！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            username = username.strip()
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['success'] = "登录成功！"
                    request.session['redirect'] = True
                    return redirect('/index/')
                else:
                    message = "密码错误！"
            except:
                message = "用户名未注册！"
        return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            phone = register_form.cleaned_data['phone']
            sex = register_form.cleaned_data['sex']

            if password1 != password2:  # 两次密码是否相同
                message = "两次输入的密码不一致！"
                return render(request, 'login/register.html', locals())
            same_name_user = models.User.objects.filter(name=username)
            if same_name_user:  # 用户名唯一
                message = '用户名已注册！'
                return render(request, 'login/register.html', locals())
            same_email_user = models.User.objects.filter(email=email)
            if same_email_user:  # 邮箱地址唯一
                message = '该邮箱已注册！'
                return render(request, 'login/register.html', locals())
            same_phone_user = models.User.objects.filter(phone=phone)
            if same_phone_user:  # 邮箱地址唯一
                message = '该手机号已注册！'
                return render(request, 'login/register.html', locals())

            new_user = models.User.objects.create()
            new_user.name = username
            new_user.password = password1
            new_user.email = email
            new_user.phone = phone
            new_user.sex = sex
            new_user.save()
            request.session['success'] = "注册成功！"
            request.session['redirect'] = True
            return redirect('/index/')
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()
    request.session['success'] = "退出成功！"
    request.session['redirect'] = True
    return redirect("/index/")
