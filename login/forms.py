# login/forms.py
from django import forms

from login import models


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=128,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))


class TaskForm1(forms.Form):
    templates = (
        (1, '任务模板1：设定问题和选项'),
        (2, '任务模板2：画标注框'),
    )
    template = forms.ChoiceField(label='任务模板', choices=templates, required=True, widget=forms.RadioSelect())


class TaskForm2(forms.Form):
    # 仅针对模版1的标注问题,暂时设定问题为1个，选项数最多为5个，可以根据需要修改
    # q1 = forms.CharField(label='问题1', max_length=128, required=True,
    #                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a1_q1 = forms.CharField(label='选项1', max_length=128, required=True,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a2_q1 = forms.CharField(label='选项2', max_length=128, required=True,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a3_q1 = forms.CharField(label='选项3', max_length=128, required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a4_q1 = forms.CharField(label='选项4', max_length=128, required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a5_q1 = forms.CharField(label='选项5', max_length=128, required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))

    # q2 = forms.CharField(label='标注问题2', max_length=128, required=False,
    #                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a1_q2 = forms.CharField(label='选项1', max_length=128, required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a2_q2 = forms.CharField(label='选项2', max_length=128, required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a3_q2 = forms.CharField(label='选项3', max_length=128, required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a4_q2 = forms.CharField(label='选项4', max_length=128, required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a5_q2 = forms.CharField(label='选项5', max_length=128, required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    #
    # q3 = forms.CharField(label='标注问题3', max_length=128, required=False,
    #                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a1_q3 = forms.CharField(label='选项1', max_length=128, required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a2_q3 = forms.CharField(label='选项2', max_length=128, required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a3_q3 = forms.CharField(label='选项3', max_length=128, required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a4_q3 = forms.CharField(label='选项4', max_length=128, required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    # a5_q3 = forms.CharField(label='选项5', max_length=128, required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))

    # 可以一次上传多张图片
    image = forms.ImageField(label='请选择图像文件', required=False,
                             widget=forms.ClearableFileInput({'multiple': True, 'style': 'font-size: 22px;'}))


class TaskForm3(forms.Form):
    name = forms.CharField(label="任务名", max_length=128, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))


class TaskForm4(forms.Form):
    users = forms.ModelMultipleChoiceField(label="选择用户", queryset=models.User.objects.filter(is_admin=False),
                                           required=False, widget=forms.CheckboxSelectMultiple())


class TaskForm5(forms.Form):
    details = forms.CharField(label="任务详情", max_length=1024, required=False,
                              widget=forms.Textarea(attrs={'class': 'form-control'}))
