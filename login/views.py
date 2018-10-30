# login/views.py
import hashlib
import json

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

from login import forms
from login import models


def gen_md5(s, salt='login'):  # 加盐
    s += salt
    md5 = hashlib.md5()
    md5.update(s.encode(encoding='utf-8'))  # update方法只接收bytes类型
    return md5.hexdigest()


def index(request):
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        messages.warning(request, "请勿重复登录！")
        return redirect("/index/")

    if request.method == "POST":
        if 'regist' in request.POST:
           return redirect("/index/")
        login_form = forms.LoginForm(request.POST)
        if not login_form.is_valid():
                   render(request, 'login/login.html', locals())

        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']

        if models.Admin.objects.filter(name=username).exists():
            group = 'admin'
            admin = models.Admin.objects.get(name=username)
            if admin.password != gen_md5(password, username):
                messages.error(request, "密码错误！")
                return render(request, 'login/login.html', locals())
        elif models.User.objects.filter(name=username).exists():
            group = 'user'
            user = models.User.objects.get(name=username)
            if user.password != gen_md5(password, username):
                messages.error(request, "密码错误！")
                return render(request, 'login/login.html', locals())
        else:
            messages.error(request, "用户名未注册！")
            return render(request, 'login/login.html', locals())

        request.session['is_login'] = True
        request.session['group'] = group
        request.session['username'] = username
        messages.success(request, "登录成功！")
        request.session.set_expiry(3600)
        return redirect('/task/')

    login_form = forms.LoginForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        messages.warning(request, "请先退出后再注册！")
        return redirect("/index/")

    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        if not register_form.is_valid():
            messages.error(request, "表单信息有误！")
            return render(request, 'login/register.html', locals())

        username = register_form.cleaned_data['username']
        password1 = register_form.cleaned_data['password1']
        password2 = register_form.cleaned_data['password2']
        email = register_form.cleaned_data['email']
       # phone = register_form.cleaned_data['phone']
      #  sex = register_form.cleaned_data['sex']

        if password1 != password2:  # 两次密码是否相同
            messages.error(request, "两次输入的密码不一致！")
            return render(request, 'login/register.html', locals())
        if models.Admin.objects.filter(name=username).exists() or \
                models.User.objects.filter(name=username).exists():  # 用户名是否唯一
            messages.error(request, "该用户名已注册！")
            return render(request, 'login/register.html', locals())
        if models.Admin.objects.filter(email=email).exists() or \
                models.User.objects.filter(email=email).exists():  # 邮箱地址是否唯一
            messages.error(request, "该邮箱已注册！")
            return render(request, 'login/register.html', locals())
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
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        messages.warning(request, "您尚未登录！")
        return redirect("/index/")

    request.session.flush()
    messages.success(request, "退出成功！")
    return redirect("/index/")


def task(request):
    if not request.session.get('is_login', None):
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")

    return render(request, 'login/task.html', locals())


def add_task(request):
    if not request.session.get('group', None) == 'admin':
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")

    if request.method == "POST":
        task_form = forms.TaskForm(request.POST)
        if not task_form.is_valid():
            messages.error(request, "表单信息有误！")
            return render(request, 'login/add_task.html', locals())

        name = task_form.cleaned_data['name']
        users_list = task_form.cleaned_data['users']
        details = task_form.cleaned_data['details']

        if models.Task.objects.filter(name=name).exists():
            messages.error(request, "该任务已存在！")
            return render(request, 'login/add_task.html', locals())

        new_task = models.Task.objects.create()
        new_task.name = name
        new_task.details = details
        new_task.admin = models.Admin.objects.get(name=request.session.get('username', None))
        new_task.save()
        for user in users_list:
            new_task.users.add(models.User.objects.get(name=user))

        messages.success(request, "任务发布成功！")
        return redirect('/task/')

    task_form = forms.TaskForm()
    return render(request, 'login/add_task.html', locals())


def get_all_tasks(request):
    if not request.session.get('group', None) == 'admin':
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")

    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    search = request.GET.get('search')
    sort_column = request.GET.get('sort')
    order = request.GET.get('order')

    if search:
        all_records = models.Task.objects.filter(name__contains=search)
    else:
        all_records = models.Task.objects.all()

    if sort_column:
        sort_column = sort_column.replace('task_', '')
        if sort_column in ['name', 'admin', 'c_time']:
            if order == 'desc':
                sort_column = '-%s' % sort_column
            all_records = all_records.order_by(sort_column)

    if not offset:
        offset = 0
    if not limit:
        limit = 10

    paginator = Paginator(all_records, limit)
    page = int(int(offset) / int(limit) + 1)
    response_data = {'total': all_records.count(), 'rows': []}

    for per_task in paginator.page(page):
        users_list = []
        for user in per_task.users.all():
            users_list.append(user.name)
        response_data['rows'].append({
            'task_name': per_task.name if per_task.name else '',
            'task_admin': per_task.admin.name if per_task.admin else '',
            'task_users': users_list if per_task.users else '',
            'task_c_time': timezone.localtime(per_task.c_time).ctime() if per_task.c_time else '',
            'task_details': per_task.details if per_task.details else '',
        })

    return HttpResponse(json.dumps(response_data))


def get_user_tasks(request):
    if not request.session.get('group', None) == 'user':
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")

    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    search = request.GET.get('search')
    sort_column = request.GET.get('sort')
    order = request.GET.get('order')

    current_user = models.User.objects.get(name=request.session.get('username', None))

    if search:
        all_records = current_user.task_set.filter(name__contains=search)
    else:
        all_records = current_user.task_set.all()

    if sort_column:
        sort_column = sort_column.replace('task_', '')
        if sort_column in ['name', 'admin', 'c_time']:
            if order == 'desc':
                sort_column = '-%s' % sort_column
            all_records = all_records.order_by(sort_column)

    if not offset:
        offset = 0
    if not limit:
        limit = 10

    paginator = Paginator(all_records, limit)
    page = int(int(offset) / int(limit) + 1)
    response_data = {'total': all_records.count(), 'rows': []}
    for per_task in paginator.page(page):
        response_data['rows'].append({
            'task_name': per_task.name if per_task.name else '',
            'task_admin': per_task.admin.name if per_task.admin.name else '',
            'task_c_time': timezone.localtime(per_task.c_time).ctime() if per_task.c_time else '',
            'task_details': per_task.details if per_task.details else '',
        })

    return HttpResponse(json.dumps(response_data))
