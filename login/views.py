# login/views.py
import json

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Sum

from login import forms
from login import models


def index(request):
    if not request.session.get('redirect', None):
        try:
            del request.session['message']
            del request.session['redirect']
        except KeyError:
            pass
    else:
        request.session['redirect'] = False

    return render(request, 'login/index.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")

    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        if not login_form.is_valid():
            return render(request, 'login/login.html', locals())

        username = login_form.cleaned_data['username'].strip()
        password = login_form.cleaned_data['password']
        group = login_form.cleaned_data['group']

        if group == 'user':
            try:
                user = models.User.objects.get(name=username)
            except:
                error_message = "用户名未注册！"
                return render(request, 'login/login.html', locals())
            if user.password != password:
                error_message = "密码错误！"
                return render(request, 'login/login.html', locals())
        else:
            try:
                admin = models.Admin.objects.get(name=username)
            except:
                error_message = "用户名未注册！"
                return render(request, 'login/login.html', locals())
            if admin.password != password:
                error_message = "密码错误！"
                return render(request, 'login/login.html', locals())

        request.session['is_login'] = True
        request.session['group'] = group
        request.session['username'] = username
        request.session['message'] = "登录成功！"
        request.session['redirect'] = True
        request.session.set_expiry(3600)
        return redirect('/task/')

    login_form = forms.LoginForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect("/index/")

    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        if not register_form.is_valid():
            return render(request, 'login/register.html', locals())

        username = register_form.cleaned_data['username']
        password1 = register_form.cleaned_data['password1']
        password2 = register_form.cleaned_data['password2']
        email = register_form.cleaned_data['email']
        phone = register_form.cleaned_data['phone']
        sex = register_form.cleaned_data['sex']

        if password1 != password2:  # 两次密码是否相同
            error_message = "两次输入的密码不一致！"
            return render(request, 'login/register.html', locals())
        same_name_user = models.User.objects.filter(name=username)
        if same_name_user:  # 用户名是否唯一
            error_message = '该用户名已注册！'
            return render(request, 'login/register.html', locals())
        same_email_user = models.User.objects.filter(email=email)
        if same_email_user:  # 邮箱地址是否唯一
            error_message = '该邮箱已注册！'
            return render(request, 'login/register.html', locals())
        same_phone_user = models.User.objects.filter(phone=phone)
        if same_phone_user:  # 手机号是否唯一
            error_message = '该手机号已注册！'
            return render(request, 'login/register.html', locals())

        new_user = models.User.objects.create()
        new_user.name = username
        new_user.password = password1
        new_user.email = email
        new_user.phone = phone
        new_user.sex = sex
        new_user.save()

        request.session['message'] = "注册成功！"
        request.session['redirect'] = True
        return redirect('/login/')

    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")

    request.session.flush()
    request.session['message'] = "退出成功！"
    request.session['redirect'] = True

    return redirect("/index/")


def task(request):
    if not request.session.get('redirect', None):
        try:
            del request.session['message']
            del request.session['redirect']
        except KeyError:
            pass
    else:
        request.session['redirect'] = False

    if request.session.get('group', None) == 'admin':
        pass
    elif request.session.get('group', None) == 'user':
        pass

    return render(request, 'login/task.html', locals())


def show_all_tasks(request):
    print(request.GET)
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    search = request.GET.get('search')
    sort_column = request.GET.get('sort')
    order = request.GET.get('order')

    if not offset:
        offset = 0
    if not limit:
        limit = 20

    if search:
        all_records = models.Task.objects.filter(name=search)
    else:
        all_records = models.Task.objects.all()

    if sort_column:
        sort_column = sort_column.replace('task_', '')
        if sort_column in ['name', 'admin']:  # 如果排序的列表在这些内容里面
            if order == 'desc':
                sort_column = '-%s' % sort_column
            all_records = all_records.order_by(sort_column)

    paginator = Paginator(all_records, limit)
    page = int(int(offset) / int(limit) + 1)
    response_data = {'total': all_records.count(), 'rows': []}

    for task in paginator.page(page):
        response_data['rows'].append({
            "task_name": task.name if task.name else "",
            "task_admin": task.admin if task.admin else "",
            "task_user": task.user if task.user else "",
        })

    return HttpResponse(json.dumps(response_data))
