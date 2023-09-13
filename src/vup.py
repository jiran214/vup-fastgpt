#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 11:06
# @Author  : 雷雨
# @File    : brain.py
# @Desc    :
from typing import List

import numpy as np
import openai
from bilibili_api import sync
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import SystemMessage, HumanMessage
import config
from langchain.chat_models import ChatOpenAI

from react.vts import VTSOperator
from utils.limit import KeyManager, inject_param_decorator
from utils.utils import top_n_indices_from_embeddings

gpt_cfg = config.speech_text_params['gpt']
gpt_cfg['openai_proxy'] = config.proxy


key_manager = KeyManager([key for key in config.openai_key_list if key])
openai.ChatCompletion.create = inject_param_decorator(api_key=key_manager.assign)(openai.ChatCompletion.create)
openai.Embedding.create = inject_param_decorator(api_key=key_manager.assign)(openai.Embedding.create)
chat_model = ChatOpenAI(**gpt_cfg, openai_api_key='temp')
Embedding = OpenAIEmbeddings(model= "text-embedding-ada-002", openai_api_key='temp')


class Brain:
    def think(self, input_text):
        # 使用Fastgpt不需要 SystemMessage(content="...", additional_kwargs={}),
        messages = [
            HumanMessage(content=input_text)
        ]
        chat_model_res = chat_model.generate([messages])
        output_text = chat_model_res.generations[0][0].text
        return output_text

class Mouth:
    def speak(self):
        ...


class Body:

    def __init__(self, live2D_actions, live2D_embeddings, vts_opt: VTSOperator):
        self.live2D_actions = live2D_actions
        self.live2D_embeddings = live2D_embeddings
        self.vts_opt = vts_opt

    def feel(self, input_text):
        txt_embedding = Embedding.embed_query(input_text)
        action_name = self.live2D_actions[
            int(top_n_indices_from_embeddings(txt_embedding, self.live2D_embeddings, top=1)[0])
        ]
        return action_name

    def action(self, action_name):
        sync(self.vts_opt.play_action(action_name))
