#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 11:06
# @Author  : 雷雨
# @File    : brain.py
# @Desc    :
import time

from bilibili_api import sync
from langchain.schema import SystemMessage, HumanMessage

import config
from utils.concurrent import Thread
from utils.utils import top_n_indices_from_embeddings

from modules import tts, llm
from modules.vts import VTSOperator


class Brain:
    def think(self, input_text, **model_kwargs):
        # 使用Fastgpt不需要 SystemMessage
        messages = []
        if system := config.llm_params['prompt']['system']:
            messages.append(SystemMessage(content=system, additional_kwargs={}),)
        messages.append(HumanMessage(content=input_text))
        chat_model_res = llm.chat_model.generate([messages], **model_kwargs)
        output_text = chat_model_res.generations[0][0].text
        return output_text


class Mouth:
    def speak(self, speech_text):
        Thread(
            lambda: tts.play_sound(sync(tts.tts_save(speech_text)))
        )


class Body:

    def __init__(self):
        vts_opt = sync(VTSOperator.init())
        self.live2D_actions = vts_opt.live2D_actions
        self.live2D_embeddings = llm.Embedding.embed_documents(texts=vts_opt.live2D_actions)
        self.vts_opt = vts_opt
        self.action_name = None

    def feel(self, input_text):
        txt_embedding = llm.Embedding.embed_query(input_text)
        action_name = self.live2D_actions[
            int(top_n_indices_from_embeddings(txt_embedding, self.live2D_embeddings, top=1)[0])
        ]
        self.action_name = action_name

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
