# login/views.py
import json

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

from login import forms
from login import models
import re

digit = re.compile("^\d{1,10}$")


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.session.get('is_login', None):
        # messages.warning(request, "请勿重复登录！")
        return redirect("/index/")

    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        if not login_form.is_valid():
            messages.error(request, "表单信息有误！")
            render(request, 'login.html', locals())

        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']

        user = models.User.objects.filter(name=username).first()
        if not user:
            messages.error(request, "用户名未注册！")
            return render(request, 'login.html', locals())
        if user.password != models.gen_md5(password, username):
            messages.error(request, "密码错误！")
            return render(request, 'login.html', locals())

        request.session['is_login'] = True
        # request.session['is_admin'] = user.is_admin
        request.session['is_admin'] = True
        request.session['username'] = username
        # messages.success(request, "登录成功！")
        request.session.set_expiry(3600)
        user.last_login_time = user.login_time
        user.login_time = timezone.now()
        user.save()
        return redirect('/all_task/')

    login_form = forms.LoginForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # messages.warning(request, "请先退出后再注册！")
        return redirect("/index/")

    if request.method == "POST":
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
        new_user.password = models.gen_md5(password1, username)
        new_user.email = email
        new_user.is_admin = False  # 只能注册普通用户
        new_user.save()

        request.session['is_login'] = True  # 注册后自动登录
        # request.session['is_admin'] = user.is_admin
        request.session['is_admin'] = True
        request.session['username'] = username
        request.session.set_expiry(3600)
        messages.success(request, "注册成功！")
        new_user.last_login_time = new_user.login_time = timezone.now()
        new_user.save()
        return redirect('/index/')

    register_form = forms.RegisterForm()
    return render(request, 'regist.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # messages.warning(request, "您尚未登录！")
        return redirect("/index/")

    request.session.flush()
    messages.success(request, "退出成功！")
    return redirect("/index/")


def release_task(request):
    if not request.session.get('is_admin', None):
        # messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")

    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        task_form = forms.TaskForm(request.POST, request.FILES)
        if not task_form.is_valid():
            messages.error(request, "表单信息有误，请重新填写！")
            return render(request, 'release_task.html', locals())

        img_files = request.FILES.getlist('image')  # exception
        print(img_files)
        print(type(img_files))

        template = task_form.cleaned_data['template']
        name = task_form.cleaned_data['name']
        details = task_form.cleaned_data['details']
        # max_tagged_num = task_form.cleaned_data['max_tagged_num']
        # credit = task_form.cleaned_data['credit']
        # print(max_tagged_num, credit)  # ##################
        # max_tagged_num = int(max_tagged_num)
        # credit = int(credit)
        max_tagged_num = 3
        credit = 2
        current_user = models.User.objects.get(name=request.session['username'])
        if current_user.total_credits < credit * len(img_files):
            messages.error(request, "您的信用积分不足，无法发布任务！")
            return render(request, 'release_task.html', locals())
        current_user.total_credits -= credit * max_tagged_num * len(img_files)
        current_user.save()

        new_task = models.Task.objects.create()
        new_task.admin = current_user
        new_task.template = int(template)
        new_task.name = name
        new_task.details = details
        new_task.max_tagged_num = max_tagged_num
        new_task.credit = credit

        # save questions and answers
        i = 1
        content = ''
        while 'q' + str(i) in request.POST:
            question = request.POST.get('q' + str(i))
            if len(question) == 0 or len(question) > 128:
                messages.error(request, "表单信息有误，请重新填写！")
                return render(request, 'release_task.html', locals())
            content += '|' + question
            j = 1
            while 'a' + str(j) + '_q' + str(i) in request.POST:
                answer = request.POST.get('a' + str(j) + '_q' + str(i))
                if len(answer) == 0 or len(answer) > 128:
                    messages.error(request, "表单信息有误，请重新填写！")
                    return render(request, 'release_task.html', locals())
                content += '&' + answer
                j += 1
            i += 1
        new_task.content = content
        new_task.save()

        # save images
        for f in img_files:
            sub_task = models.SubTask.objects.create()
            sub_task.image = f
            sub_task.task = new_task
            sub_task.save()
            # label = models.Label.objects.create()
            # label.sub_task = sub_task
            # label.save()

        # messages.success(request, "任务发布成功！")
        return redirect('/all_task/')

    task_form = forms.TaskForm()
    return render(request, 'release_task.html', locals())


def collect_task(request):
    if not request.session.get('is_login', None) or not digit.match(request.POST.get('collect')):
        print('用户未登录或该task_id不合法！')
        return
    task_id = int(request.POST.get('collect'))
    favorite_task = models.Task.objects.filter(pk=task_id).first()
    if not favorite_task:
        print('该任务不存在！')
        return
    current_user = models.User.objects.get(name=request.session['username'])
    current_user.favorite_tasks.add(favorite_task)


def remove_task(request):
    if not request.session.get('is_login', None):
        return
    current_user = models.User.objects.get(name=request.session['username'])
    task_id_list = request.POST.getlist('removed_task_id_list')
    for task_id in task_id_list:
        if not digit.match(task_id):
            print('该task_id不合法！')
            continue
        task_id = int(task_id)
        task = models.Task.objects.filter(pk=task_id).first()
        if not task:
            print('该任务不存在！')
            continue
        current_user.favorite_tasks.remove(task)  # when not exist, no exception.


def cancel_task(request):
    if not request.session.get('is_login', None):
        return
    # current_user = models.User.objects.get(name=request.session['username'])
    task_id_list = request.POST.getlist('canceled_task_id_list')
    for task_id in task_id_list:
        if not digit.match(task_id):
            print('该task_id不合法！')
            continue
        task_id = int(task_id)
        models.Task.objects.filter(pk=task_id).delete()
        # task = models.Task.objects.filter(pk=task_id).first()
        # if not task:
        #     print('该任务不存在！')
        #     continue
        # task.is_closed = True
        # task.save()


def all_task(request):
    task_list = models.Task.objects.all()
    num_task = task_list.count()
    num_user = models.User.objects.count()
    template_list = ['', '问答式', '标记式', '书写式']
    temp_excluded_list = []

    if request.method == "POST":
        print(request.POST)
        if 'task_sort' in request.POST or 'task_filter' in request.POST:
            if request.POST.get('order') == 'time_desc':
                task_list = task_list.order_by('-c_time')
            temp_excluded_list = request.POST.getlist('temp_excluded')
            if 'temp1' in temp_excluded_list:
                task_list = task_list.exclude(template=1)
            if 'temp2' in temp_excluded_list:
                task_list = task_list.exclude(template=2)
            if 'temp3' in temp_excluded_list:
                task_list = task_list.exclude(template=3)
            if request.POST.get('tagged_num') == 'single':
                task_list = task_list.filter(max_tagged_num=1)
            elif request.POST.get('tagged_num') == 'multi':
                task_list = task_list.exclude(max_tagged_num=1)
        elif 'collect' in request.POST:
            collect_task(request)
        elif 'remove' in request.POST:
            remove_task(request)
        elif 'enter' in request.POST:
            if digit.match(request.POST.get('enter')):
                request.session['task_id'] = int(request.POST.get('enter'))
                return redirect('/enter_task/')
        elif 'cancel_tasks' in request.POST:
            cancel_task(request)
            task_list = models.Task.objects.all()
            num_task = task_list.count()
        elif 'review' in request.POST:
            if digit.match(request.POST.get('review')):
                request.session['task_id'] = int(request.POST.get('review'))
                return redirect('/one_task/')

    if request.session.get('is_login', None):
        current_user = models.User.objects.get(name=request.session['username'])
        favorite_task_list = current_user.favorite_tasks.all()
        num_favorite_task = favorite_task_list.count()
        released_task_list = current_user.released_tasks.all()
        num_released_task = released_task_list.count()

        current_user.login_time = timezone.now()
        current_user.save()
        num_updated_task = models.Task.objects.filter(c_time__gt=current_user.last_login_time).count()
        # num_task_unfinished = models.Task.objects.filter(is_closed=False).count()

    return render(request, 'all_task.html', locals())


def enter_task(request):
    if not request.session.get('is_login', None) or not request.session.get('task_id', None):
        return redirect('/all_task/')
    current_user = models.User.objects.get(name=request.session['username'])
    task = models.Task.objects.get(id=request.session['task_id'])

    if request.method == "POST":
        print(request.POST)
        i = 1
        result = ''
        while 'q' + str(i) in request.POST:
            result += '|' + 'q' + str(i)
            answers = request.POST.getlist('q' + str(i))
            for answer in answers:
                result += '&' + answer
            i += 1
        sub_task_id = request.session.get('sub_task_id', None)
        if sub_task_id:
            sub_task = models.SubTask.objects.get(pk=sub_task_id)
            print(sub_task)
            label = models.Label.objects.create()
            label.user = current_user
            label.result = result
            label.sub_task = sub_task
            label.save()
            sub_task.num_tagged += 1
            sub_task.users.add(current_user)
            sub_task.save()
            current_user.total_credits += task.credit
            current_user.save()
            request.session['sub_task_id'] = None

    qa_list = []
    contents = task.content.split('|')
    for item in contents[1:]:
        qa = item.split('&')
        qa_list.append({'question': qa[0], 'answers': qa[1:]})
    sub_task = models.get_untagged_sub_task(task, current_user)
    if sub_task:
        request.session['sub_task_id'] = sub_task.id
        img_file = sub_task.image
        print(img_file)
    else:
        print('所有图片已标注')
    return render(request, 'enter_task.html', locals())


def check_task(request):
    if not request.session.get('is_login', None) or not request.session.get('task_id', None) or not request.session.get(
            'sub_task_id', None):
        return redirect('/all_task/')
    current_user = models.User.objects.get(name=request.session['username'])
    task = models.Task.objects.get(id=request.session['task_id'])
    sub_task = models.SubTask.objects.get(id=request.session['sub_task_id'])
    label_list = sub_task.label_set.all()

    qa_list = []
    contents = task.content.split('|')
    for i, item in enumerate(contents[1:]):
        qa = item.split('&')
        answers = []
        for ans in qa[1:]:
            answers.append([ans, 0])
        for label in label_list:
            ans_list = label.result.split('|')[i+1].split('&')[1:]
            for j, ans in enumerate(ans_list):
                answers[int(ans)-1][1] += 1
        qa_list.append({'question': qa[0], 'answers': answers})

    return render(request, 'check_task.html', locals())


def one_task(request):
    if not request.session.get('is_login', None) or not request.session.get('task_id', None):
        return redirect('/all_task/')
    current_user = models.User.objects.get(name=request.session['username'])
    task = models.Task.objects.get(id=request.session['task_id'])

    if request.method == "POST" and 'enter' in request.POST:
        if digit.match(request.POST.get('enter')):
            request.session['sub_task_id'] = int(request.POST.get('enter'))  # need some check
            return redirect('/check_task/')

    sub_task_list = task.subtask_set.all()
    num_favorite_task = current_user.favorite_tasks.count()
    num_released_task = current_user.released_tasks.count()
    num_updated_task = models.Task.objects.filter(c_time__gt=current_user.last_login_time).count()
    return render(request, 'one_task.html', locals())


def recharge(request):
    if not request.session.get('is_login', None):
        return redirect('/all_task/')
    current_user = models.User.objects.get(name=request.session['username'])

    if request.method == "POST":
        print(request.POST)

    return render(request, 'recharge.html', locals())


def get_all_tasks(request):
    if not request.session.get('is_admin', None):
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
    if not request.session.get('is_login', None) or request.session.get('is_admin', None):
        messages.warning(request, "您没有权限查看该页面！")
        return redirect("/index/")

    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    search = request.GET.get('search')
    sort_column = request.GET.get('sort')
    order = request.GET.get('order')

    current_user = models.User.objects.get(name=request.session.get('username', None))

    if search:
        all_records = current_user.tasks_owned.filter(name__contains=search)
    else:
        all_records = current_user.tasks_owned.all()

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
