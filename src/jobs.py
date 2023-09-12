#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 19:19
# @Author  : 雷雨
# @File    : core.py
# @Desc    :
import threading
import time
from typing import Callable

from live_server.bilibili import BlLiveRoom
from utils import live_queue, log
from speech_text import brain
import config


class BlLiveJob:
    def __call__(self):
        r = BlLiveRoom(config.live_params['bilibili']['room_id'])
        r.connect()


class GPTJob:
    bl_cfg = config.live_params['bilibili']

    def handle(self, event):
        # step 生成gpt文本
        temple = self.bl_cfg[event['type'].value]
        prompt_temple, speech_temple = temple['prompt'], temple['speech']
        try:
            prompt = prompt_temple.format(**event)
        except Exception as e:
            log.error('模版构造错误')
            log.exception(e)
            return
        output_text = brain.think(prompt)

        # step 生成语音文本
        speech = speech_temple.format(**prompt_temple, gpt=output_text)
        return speech

    def __call__(self, *args, **kwargs):
        while True:
            t0 = time.time()
            event = live_queue.recv()
            if not event:
                # Both queues are empty, wait for new items to be added
                time.sleep(1)
                log.debug('vup waiting...')
                continue
            try:
                self.handle(event)
                log.debug(f'worker耗时:{time.time() - t0}')
            except Exception as e:
                raise e
                # log.error(e)


class ReactJob:

    def __call__(self, *args, **kwargs):
        ...


def start_thread(job: Callable):
    thread = threading.Thread(target=job)
    thread.start()
    return thread