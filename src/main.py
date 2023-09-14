#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 19:19
# @Author  : 雷雨
# @File    : main.py
# @Desc    :
import config
import threads
from utils.concurrent import start_thread


if __name__ == '__main__':
    # 初始化
    producers = [start_thread(threads.SchedulerProducer())] if config.scheduler_params else None
    producers.append(start_thread(threads.LiveProducer('bilibili')))
    consumer = start_thread(threads.VupConsumer())

    # 启动
    [producer.join() for producer in producers]
    consumer.join()
