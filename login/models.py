# login/models.py
from django.db import models
from django.utils import timezone
import hashlib


def gen_md5(s, salt='9527'):  # 加盐
    s += salt
    md5 = hashlib.md5()
    md5.update(s.encode(encoding='utf-8'))  # update方法只接收bytes类型
    return md5.hexdigest()


def img_directory_path(instance, filename):
    # 文件上传到MEDIA_ROOT/task_<id>/<filename>目录中
    return 'task_{0}/{1}'.format(instance.task.id, filename)


def get_untagged_sub_task(task, user):
<<<<<<< HEAD
    sub_task_set = task.subtask_set.filter(num_tagged__lt=task.max_tagged_num)
    for sub_task in sub_task_set:
        if not sub_task.users.filter(pk=user.id).exists():
            return sub_task
    return None
=======
    sub_task_set = task.subtask_set.exclude(users__id=user.id)
    print('sub_task_set', sub_task_set)
    return sub_task_set.first()  # if not exist, return None.


def get_rejected_sub_task(task, user):
    sub_task_set = task.subtask_set.filter(users__id=user.id)
    print('sub_task_set', sub_task_set)
    return sub_task_set.first()  # if not exist, return None.
>>>>>>> f8806b6131d127303bd540ec1cbe91cf2595d5bb


class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    c_time = models.DateTimeField(auto_now_add=True)  # 保存用户创建时间
    login_time = models.DateTimeField(default=timezone.now)  # 保存此次登录时间
    last_login_time = models.DateTimeField(default=timezone.now)  # 保存上次登录时间
<<<<<<< HEAD
    favorite_tasks = models.ManyToManyField('Task')
=======
    # favorite_tasks = models.ManyToManyField('Task')
    total_credits = models.IntegerField(default=1000)
>>>>>>> f8806b6131d127303bd540ec1cbe91cf2595d5bb

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["c_time"]


class Task(models.Model):
    """任务表"""

    template = models.IntegerField(default=1)
    content = models.TextField(max_length=1024)
    name = models.CharField(max_length=128)
<<<<<<< HEAD
    admin = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='tasks_created')
=======
    admin = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='released_tasks')
>>>>>>> f8806b6131d127303bd540ec1cbe91cf2595d5bb
    details = models.TextField(max_length=1024)
    c_time = models.DateTimeField(auto_now_add=True)
    max_tagged_num = models.IntegerField(default=1)
    is_closed = models.BooleanField(default=False)
<<<<<<< HEAD
=======
    credit = models.IntegerField(default=1)
    users = models.ManyToManyField('User', related_name='favorite_tasks', through='TaskUser')
>>>>>>> f8806b6131d127303bd540ec1cbe91cf2595d5bb

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["c_time"]


class TaskUser(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    # is_rejected = models.BooleanField(default=False)
    # is_unreviewed = models.NullBooleanField(default=None)
    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["c_time"]


class SubTask(models.Model):
    """子任务表"""

    image = models.ImageField(max_length=256, upload_to=img_directory_path)
    task = models.ForeignKey('Task', null=True, on_delete=models.CASCADE)
    result = models.TextField(max_length=1024)  # 保存最终标记结果
<<<<<<< HEAD
    num_tagged = models.IntegerField(default=0)
    users = models.ManyToManyField('User', related_name='sub_tasks_tagged')
=======
    # num_tagged = models.IntegerField(default=0)
    users = models.ManyToManyField('User', related_name='sub_tasks_tagged', through='Label')
>>>>>>> f8806b6131d127303bd540ec1cbe91cf2595d5bb


class Label(models.Model):
    """标签表"""

<<<<<<< HEAD
    sub_task = models.ForeignKey('SubTask', null=True, on_delete=models.CASCADE)
=======
    sub_task = models.ForeignKey('SubTask', on_delete=models.CASCADE, null=True)
>>>>>>> f8806b6131d127303bd540ec1cbe91cf2595d5bb
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    result = models.TextField(max_length=1024)  # 保存标记结果
    m_time = models.DateTimeField(auto_now=True)  # 保存最后标记时间
    # is_tagged = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_unreviewed = models.BooleanField(default=True)
    task_user = models.ForeignKey('TaskUser', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["m_time"]
