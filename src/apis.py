#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 19:19
# @Author  : 雷雨
# @File    : apis.py
# @Desc    :
import random
import time
from multiprocessing import Process

import config
import threads
from utils.concurrent import Thread
from typing import Optional

p: Optional[Process] = None


def get_vts():
    from modules.vts import VTSOperator
    VTSOperator.init()


def run_vup(platform):
    config.settings.flush()
    # 初始化
    producers = [Thread(threads.SchedulerProducer())] if config.settings.scheduler_params else None
    producers.append(Thread(threads.LiveProducer(platform)))
    consumer = Thread(threads.VupConsumer(platform))
    # 启动
    [producer.join() for producer in producers]
    consumer.join()


def start(platform):
    global p
    p = Process(target=run_vup, args=(platform,))
    p.start()


def stop():
    global p
    if p.is_alive:
        # stop a process gracefully
        p.terminate()
        print('stop process')
        p.join()
