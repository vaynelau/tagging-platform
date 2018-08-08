#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':
    send_mail(
        '来自www.liujiangblog.com的测试邮件',
        '欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，本站专注于Python和Django技术的分享！',
        'liu1351853931@sina.cn',
        ['liu1351853931@139.com'],
    )
