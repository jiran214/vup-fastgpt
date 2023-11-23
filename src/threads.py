#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 19:19
# @Author  : 雷雨
# @File    : core.py
# @Desc    :
import threading
import time

import schedule
from bilibili_api import sync

import config
from producers.bilibili_server import BlLiveRoom
from producers import wechat_server
from modules.vts import VTSOperator
from utils import live_queue, log
import vup
from utils.concurrent import Thread
from utils.enums import LiveInputType
from utils.filter import DFA
from utils.utils import Record


class LiveProducer:

    def __init__(self, platform, debug=False):
        self.platform = platform.lower()
        self.debug = debug

    def __call__(self):
        if self.platform == 'bilbili':
            r = BlLiveRoom(
                config.settings.live_params[self.platform]['room_id'],
                config.settings.live_params[self.platform]['credential'],
                debug=self.debug
            )
            r.connect()
        elif self.platform == 'wechat':
            wechat_server.connect()


class SchedulerProducer:
    wait_seconds = 10

    def __init__(self):
        self.scheduler = self.create()

    def create(self):
        # 清空任务
        schedule.clear()
        if not config.settings.scheduler_params:
            log.error('未发现定时任务')
            return
        for value in config.settings.scheduler_params:
            log.info(f'发现schedule调度任务-数量:{len(config.settings.scheduler_params)}-提前处理中,')
            event = {
                "type": LiveInputType.scheduler,
                **value
            }
            if frequency := value.get('frequency'):
                schedule.every(int(frequency)).seconds.do(lambda: live_queue.send(event, True))
            elif timing := value.get('timing'):
                schedule.every().day.at(timing).do(lambda: live_queue.send(event, True))
        log.info(f'调度事件创建完毕:{schedule.jobs}')
        return schedule

    def __call__(self, *args, **kwargs):
        # 延时启动
        assert self.scheduler
        time.sleep(self.wait_seconds)
        self.scheduler.run_pending()


class VupConsumer:

    dfa = DFA(config.settings.filter_words)
    log.debug(f"加载违禁词成功:数量{len(config.settings.filter_words)}-预览：{str(config.settings.filter_words[:10])}...")

    def __init__(self, platform):
        assert platform in ('wechat', 'bilibili')
        self.vup = vup.VTuber()
        self.platform = platform
        self.live_cfg = config.settings.live_params

    def handle(self, event):
        model_kwargs = {}
        # step 生成gpt文本
        log.info('step1:生成prompt')
        t0 = time.time()
        if event['type'] == LiveInputType.scheduler:
            # 调度任务处理
            temple = event
            model_kwargs = {'max_tokens': None}
        else:
            # 弹幕服务器处理
            temple = self.live_cfg[event['type'].value]

        prompt_temple, speech_temple = temple['prompt'], temple['speech']
        try:
            prompt = prompt_temple.format(**event)
        except Exception as e:
            log.error(f'模版构造错误 event:{event}')
            log.exception(e)
            return

        # step 违禁词过滤
        if words := self.dfa.match(prompt):
            log.warning(f'触发违禁词过滤-prompt:{prompt}-words:{words}')
            return

        log.info('step2:生成动作')
        action_thread = Thread(self.vup.body.feel(prompt)) if self.vup.body else None

        log.info('step3:生成语音文本')
        output_text = self.vup.brain.think(prompt, **model_kwargs)
        speech = speech_temple.format(**event, gpt=output_text)
        # step 违禁词过滤
        if words := self.dfa.match(speech):
            log.warning(f'触发违禁词过滤-speech:{speech}-words:{words}')
            return

        log.info('step4:播放语音和动作')
        self.vup.mouth.speak(speech)

        if self.vup.body:
            action_thread.join()
            self.vup.body.action(self.vup.body.action_name)

        # step 存档
        cost_time = str(time.time() - t0)[:4]
        record = Record(
            event=event,
            prompt=prompt,
            speech=speech,
            action=self.vup.body and self.vup.body.action_name,
            time=cost_time
        )
        log.info(f'step end:{record}')

    def __call__(self):
        while True:
            event = live_queue.recv()
            log.info(f'step0:收到生产者消息:{event}')
            try:
                self.handle(event)
            except Exception as e:
                raise e
                # log.error(e)


