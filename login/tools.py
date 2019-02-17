#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import cv2
import os

from mysite.settings import MEDIA_ROOT
from login import models


def video2pictures(task, frame_interval=10):
    # 包含视频片段的路径
    input_path = os.sep.join([MEDIA_ROOT, 'task_{}'.format(task.id)])

    # 初始化一个VideoCapture对象
    cap = cv2.VideoCapture()

    # 遍历所有文件
    for sub_task in task.subtask_set.all():
        sub_task.screenshot_set.all().delete()
        file_path = os.sep.join([MEDIA_ROOT, sub_task.file.name])
        print(file_path)
        frame_path = os.sep.join([input_path, str(sub_task.id)])
        print(frame_path)

        if not os.path.exists(frame_path):
            os.mkdir(frame_path)

        # VideoCapture::open函数可以从文件获取视频
        cap.open(file_path)

        # 获取视频帧数
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # 同样为了避免视频头几帧质量低下，黑屏或者无关等
        for i in range(42):
            cap.read()

        cnt = 1
        for i in range(n_frames - 42):
            ret, img = cap.read()

            # 每隔frame_interval帧进行一次截屏操作
            if i % frame_interval == 0:
                image_name = '{:0>6d}.jpg'.format(cnt)
                cnt += 1
                image_path = os.sep.join([frame_path, image_name])
                print('exported {}!'.format(image_path))
                cv2.imwrite(image_path, img)
                screenshot = models.Screenshot.objects.create()
                screenshot.sub_task = sub_task
                screenshot.image = image_path
                screenshot.save()
    # 执行结束释放资源
    cap.release()


def draw(sub_task, label, pos):
    img_path = os.sep.join([MEDIA_ROOT, sub_task.file.name])
    label_dir = img_path.split('.')[0]
    print(label_dir)
    if not os.path.exists(label_dir):
        os.mkdir(label_dir)
    new_img_path = os.sep.join([label_dir, '{:0>8d}.jpg'.format(label.id)])
    img = cv2.imread(img_path)
    print(img_path)
    pos_list = pos.split('|')
    for pos in pos_list[:-1]:
        p = pos.split('&')[1].split(',')
        cv2.rectangle(img, (int(p[0]), int(p[1])), (int(p[2]), int(p[3])), (0, 255, 0), 1)
    cv2.imwrite(new_img_path, img)


def draw_2(sub_task, label, pos):
    # img_path = os.sep.join([MEDIA_ROOT, sub_task.file.name])
    # label_dir = img_path.split('.')[0]
    # print(label_dir)
    # if not os.path.exists(label_dir):
    #     os.mkdir(label_dir)
    # new_img_path = os.sep.join([label_dir, '{:0>8d}.jpg'.format(label.id)])
    # img = cv2.imread(img_path)
    # print(img.shape)
    # pos_list = pos.split('|')
    # for pos in pos_list[:-1]:
    #     p = pos.split('&')[1].split(',')
    #     cv2.rectangle(img, (int(p[0]), int(p[1])), (int(p[2]), int(p[3])), (0, 255, 0), 1)
    # cv2.imwrite(new_img_path, img)
    pass