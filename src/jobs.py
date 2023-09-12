#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 19:19
# @Author  : 雷雨
# @File    : core.py
# @Desc    :
import asyncio
import threading
import time
from typing import Callable

from bilibili_api import sync

from live_server.bilibili import BlLiveRoom
from utils import live_queue, log
from speech_text import brain
from react import tts
import config
from utils.concurrent import start_thread
from utils.utils import Record


class LiveJob:

    def __init__(self, platform, debug=False):
        self.platform = platform
        self.debug = debug

    def __call__(self):
        r = BlLiveRoom(
            config.live_params[self.platform]['room_id'],
            config.live_params[self.platform]['credential'],
            debug=self.debug
        )
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
        speech = speech_temple.format(**event, gpt=output_text)
        return speech, prompt

    def __call__(self):
        while True:
            event = live_queue.recv()
            if not event:
                time.sleep(1)
                log.debug('no event vup waiting...')
                continue
            try:
                t0 = time.time()
                speech, prompt = self.handle(event)
                start_thread(lambda: ReactJob()(speech))
                cost_time = str(time.time() - t0)[:4]
                record = Record(
                    prompt=prompt,
                    speech=speech,
                    time=cost_time
                )
                log.info(f'完成一轮回应:{record}')
            except Exception as e:
                raise e
                # log.error(e)


class ReactJob:

    def __call__(self, speech_text):
        path = sync(tts.tts_save(speech_text))
        tts.play_sound(path)

