#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import cv2
import os

from mysite.settings import MEDIA_ROOT


def video2pictures(task, frame_interval=10):
    # 包含视频片段的路径
    input_path = os.sep.join([MEDIA_ROOT, 'task_{}'.format(task.id)])

    # 列出文件夹下所有的视频文件
    file_names = os.listdir(input_path)

    # 建立一个新的文件夹，名称为原文件夹名称后加上_frames
    # frame_path = '{}_frames'.format(input_path)
    frame_path = os.sep.join([input_path, 'frames'])
    print(frame_path)

    if not os.path.exists(frame_path):
        os.mkdir(frame_path)
    else:
        frames = os.listdir(frame_path)
        for frame in frames:
            os.remove(os.sep.join([frame_path, frame]))

    # 初始化一个VideoCapture对象
    cap = cv2.VideoCapture()

    # 遍历所有文件
    for file_name in file_names:
        file_path = os.sep.join([input_path, file_name])

        # VideoCapture::open函数可以从文件获取视频
        cap.open(file_path)

        # 获取视频帧数
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # 同样为了避免视频头几帧质量低下，黑屏或者无关等
        for i in range(42):
            cap.read()

        for i in range(n_frames - 42):
            ret, frame = cap.read()

            # 每隔frame_interval帧进行一次截屏操作
            if i % frame_interval == 0:
                image_name = '{}_{:0>6d}.jpg'.format(file_name.split('.')[0], i)
                image_path = os.sep.join([frame_path, image_name])
                print('exported {}!'.format(image_path))
                cv2.imwrite(image_path, frame)

    # 执行结束释放资源
    cap.release()
