#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 19:19
# @Author  : 雷雨
# @File    : main.py
# @Desc    :
import config
import threads
from utils.concurrent import Thread


if __name__ == '__main__':
    # platform = 'wechat'
    platform = 'bilibili'

    # 初始化
    producers = [Thread(threads.SchedulerProducer())] if config.scheduler_params else None
    # producers.append(Thread(threads.LiveProducer(platform)))
    consumer = Thread(threads.VupConsumer(platform))

    # 启动
    [producer.join() for producer in producers]
    consumer.join()
