#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 12:03
# @Author  : 雷雨
# @File    : queues.py
# @Desc    :
import queue
import time
from typing import Union


class LiveQueue:
    def __init__(self, maxsize=15):
        self.event_queue = queue.Queue(maxsize)
        self.high_event_queue = queue.Queue()

    def send(self, event: Union[dict, None], is_high_event=False):
        if is_high_event:
            self.high_event_queue.put_nowait(event)
        else:
            if not self.event_queue.full():
                self.event_queue.put_nowait(event)
            else:
                self.event_queue.put(event)

    def recv(self) -> Union[None, dict]:
        if self.high_event_queue.not_empty:
            event = self.high_event_queue.get()
        elif not self.event_queue.empty():
            event = self.event_queue.get()
        else:
            time.sleep(1)
            return self.recv()
        return event
