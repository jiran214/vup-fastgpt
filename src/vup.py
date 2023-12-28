#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from langchain.schema import SystemMessage, HumanMessage

import config
from utils import log
from modules import tts, llm
from modules.vts import VTSOperator


class Brain:
    def think(self, input_text, **model_kwargs):
        # 使用Fastgpt不需要 SystemMessage
        messages = []
        if system := config.settings.llm_params['prompt']['system']:
            messages.append(SystemMessage(content=system, additional_kwargs={}),)
        messages.append(HumanMessage(content=input_text))
        output_text = llm.chat_model(messages).content
        return output_text


class Mouth:
    async def speak(self, speech_text):
        log.info(f'step4:播放语音:{len(speech_text)}')
        speech_text = await tts.tts_save(speech_text)
        tts.play_sound(speech_text)


class Body:

    def __init__(self):
        vts_opt = VTSOperator()
        # self.live2D_embeddings = llm.Embedding.embed_documents(texts=vts_opt.live2D_actions)
        self.vts_opt = vts_opt
        self.s = requests.Session()
        self.s.headers = {
            'Authorization': 'Bearer fastgpt-tsm3gqsbyljbf4k0bh762yps-6559dcc0ed049c3059f0e304'
        }
        self.action_name = None
        # self.loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(self.loop)

    def feel(self, input_text):
        url = 'http://ai.newhopedairy.cn/api/openapi/kb/searchTest'
        POST = {
            "kbId": "6559dcc0ed049c3059f0e304",
            "text": input_text,
            "rarank": True,
            "limit": 1
        }
        r = self.s.post(url, json=POST)
        r.raise_for_status()
        self.action_name = [action['a'].strip('动作').strip('表情') for action in r.json()['data']][0]

    async def action(self, action_name: str):
        log.info(f'step4:播放动作:{action_name}')
        if not action_name:
            action_name = None
            return
        # 等待1秒再做动作
        # await asyncio.sleep(1)
        await self.vts_opt._aplay_action(action_name)


class VTuber:
    def __init__(self):
        self.brain = Brain()
        self.mouth = Mouth()
        self.body = Body() if config.action else None


if __name__ == '__main__':
    Body().feel('我讨厌你')