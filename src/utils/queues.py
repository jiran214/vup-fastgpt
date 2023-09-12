#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 12:03
# @Author  : 雷雨
# @File    : queues.py
# @Desc    :
import queue
from typing import Union


class LiveQueue:
    def __init__(self, maxsize=15):
        self.event_queue = queue.Queue(maxsize)

    def send(self, event: Union[dict, None]):
        if not event:
            return
        else:
            if not self.event_queue.full():
                self.event_queue.put_nowait(event)
            else:
                self.event_queue.put(event)

    def recv(self) -> Union[None, dict]:
        if not self.event_queue.empty():
            event = self.event_queue.get()
        else:
            event = None
        return event