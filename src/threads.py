#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 19:19
# @Author  : 雷雨
# @File    : core.py
# @Desc    :
import asyncio
import threading
import time

import schedule
import config
from producers import wechat_server
from utils import live_queue, log
from utils.concurrent import Thread
from utils.enums import LiveInputType
from utils.filter import DFA
from utils.utils import Record


class LiveProducer:

    def __init__(self, platform, debug=False):
        self.platform = platform.lower()
        self.debug = debug

    def __call__(self):
        if self.platform == 'bilibili':
            from producers.bilibili_server import BlLiveRoom
            r = BlLiveRoom(
                config.settings.live_params[self.platform]['room_id'],
                config.settings.live_params[self.platform]['credential'],
                debug=self.debug
            )
            r.connect()
        elif self.platform == 'wechat':
            wechat_server.connect()


class SchedulerProducer:
    wait_seconds = 30

    def __init__(self):
        self.scheduler = schedule
        self.create()

    def create(self):
        # 清空任务
        self.scheduler.clear()
        if not config.settings.scheduler_params:
            log.error('未发现定时任务')
            return
        log.info(f'发现schedule调度任务-数量:{len(config.settings.scheduler_params)}-提前处理中,')
        for value in config.settings.scheduler_params:
            if not value.get('switch'):
                continue
            event = {
                "type": LiveInputType.scheduler,
                **value
            }
            if frequency := value.get('frequency'):
                self.scheduler.every(int(frequency)).minutes.do(live_queue.send, event, True)
            elif timing := value.get('timing'):
                self.scheduler.every().day.at(timing).do(live_queue.send, event, True)
        log.info(f'调度事件创建完毕:{schedule.jobs}')

    def __call__(self, *args, **kwargs):
        # 延时启动
        assert self.scheduler
        time.sleep(self.wait_seconds)
        while True:
            self.scheduler.run_pending()
            time.sleep(1)


class VupConsumer:
    vup_lock = threading.Lock()

    def __init__(self, platform):
        import vup
        assert platform in ('wechat', 'bilibili')
        self.vup = vup.VTuber()
        self.platform = platform
        self.live_cfg = config.settings.live_params
        self.dfa = DFA(config.settings.filter_words)
        self.error_times = 0
        log.debug(f"加载违禁词成功:数量{len(config.settings.filter_words)}-预览：{str(config.settings.filter_words[:10])}...")

    async def ahandle(self, event):
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
            temple = self.live_cfg['temple'][event['type'].value]

        prompt_temple, speech_temple = temple['prompt'], temple['speech']
        prompt = None
        if prompt_temple:
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
            log.info('step2:生成语音文本')
            output_text = self.vup.brain.think(prompt, **model_kwargs)
            speech_temple = speech_temple or '{gpt}'
            speech = speech_temple.format(**event, gpt=output_text)
        else:
            speech = speech_temple.format(**event)

        # step 违禁词过滤
        if words := self.dfa.match(speech):
            log.warning(f'触发违禁词过滤-speech:{speech}-words:{words}')
            return
        tasks = []
        tasks.append(asyncio.create_task(self.vup.mouth.speak(speech)))
        tasks.append(asyncio.create_task(self.vup.body.action(speech)))
        await asyncio.gather(*tasks)
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

    async def run(self):
        await self.vup.body.vts_opt.ainit()
        while True:
            event = live_queue.recv()
            if not event:
                await asyncio.sleep(1)
                continue
            log.info(f'step0:收到生产者消息:{event}')
            try:
                await self.ahandle(event)
                self.error_times = 0
            except Exception as e:
                self.error_times += 1
                if self.error_times > 3:
                    log.error(f'程序失败次数过多')
                    raise e
                log.error(f'弹幕回复异常！{e}')

    def __call__(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run())


if __name__ == '__main__':
    LiveProducer('wechat')()