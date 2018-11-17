# login/models.py
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    c_time = models.DateTimeField(auto_now_add=True)  # 保存创建时间，不可修改

    def __str__(self):
        return self.name


class Task(models.Model):
    """任务表"""

    template = models.IntegerField(default=1)
    name = models.CharField(max_length=128, unique=True)
    admin = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='tasks_created_by_the_admin')
    users = models.ManyToManyField('User', related_name='tasks_owned_by_the_user')
    details = models.TextField(max_length=1024)
    c_time = models.DateTimeField(auto_now_add=True)  # 保存创建时间，不可修改

    def __str__(self):
        return self.name


class SubTask(models.Model):
    """子任务表"""

    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    content = models.TextField(max_length=1024)  # 保存问题及选项，中以分隔符分隔
    result = models.TextField(max_length=1024)  # 保存标记结果

    def __str__(self):
        return self.content


class Label(models.Model):
    """标签表"""

    sub_task = models.ForeignKey('SubTask', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    result = models.TextField(max_length=1024)  # 保存标记结果
    m_time = models.DateTimeField(auto_now=True)  # 保存最后标记时间，可以修改
