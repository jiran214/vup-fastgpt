#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import time

import requests
from bilibili_api import sync
from langchain.schema import SystemMessage, HumanMessage

import config
from utils.concurrent import Thread

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
    def speak(self, speech_text):
        Thread(
            lambda: tts.play_sound(sync(tts.tts_save(speech_text)))
        )


class Body:

    def __init__(self):
        vts_opt = VTSOperator.init()
        self.live2D_actions = vts_opt.live2D_actions
        # self.live2D_embeddings = llm.Embedding.embed_documents(texts=vts_opt.live2D_actions)
        self.vts_opt = vts_opt
        self.s = requests.Session()
        self.s.headers = {
            'Authorization': 'Bearer fastgpt-tsm3gqsbyljbf4k0bh762yps-6559dcc0ed049c3059f0e304'
        }
        self.action_name = None

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
        self.action_name = [action['a'] for action in r.json()['data']][0]

    def action(self, action_name):
        if not action_name:
            action_name = None
            return
        Thread(lambda: (
            # 等待1秒再做动作
            time.sleep(1),
            sync(self.vts_opt.play_action(action_name))
        ))


class VTuber:
    def __init__(self):
        self.brain = Brain()
        self.mouth = Mouth()
        self.body = Body() if config.action else None


if __name__ == '__main__':
    Body().feel('我讨厌你')