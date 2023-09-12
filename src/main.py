#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 19:19
# @Author  : 雷雨
# @File    : main.py
# @Desc    :
import threading
from typing import Callable
import jobs
from utils.concurrent import start_thread

if __name__ == '__main__':
    producer = start_thread(jobs.LiveJob('bilibili'))
    consumer = start_thread(jobs.GPTJob())
    producer.join()
    consumer.join()