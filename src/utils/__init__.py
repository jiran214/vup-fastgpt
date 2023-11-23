#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 10:40
# @Author  : 雷雨
# @File    : __init__.py.py
# @Desc    :
from utils.logger import get_loguru_logger
from utils.queues import LiveQueue

log = get_loguru_logger('vup')
live_queue: LiveQueue = LiveQueue(maxsize=15)