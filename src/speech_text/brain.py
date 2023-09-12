#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 11:06
# @Author  : 雷雨
# @File    : brain.py
# @Desc    :
import openai
from langchain.schema import SystemMessage, HumanMessage

import config
from langchain.chat_models import ChatOpenAI

from utils.limit import KeyManager, inject_param_decorator

gpt_cfg = config.speech_text_params['gpt']
gpt_cfg['openai_proxy'] = config.proxy


key_manager = KeyManager([key for key in config.openai_key_list if key])
openai.ChatCompletion.create = inject_param_decorator(api_key=key_manager.assign)(openai.ChatCompletion.create)
openai.Embedding.create = inject_param_decorator(api_key=key_manager.assign)(openai.Embedding.create)
chat_model = ChatOpenAI(**gpt_cfg, openai_api_key='temp')


def think(input_text):
    # 使用Fastgpt不需要 SystemMessage(content="...", additional_kwargs={}),
    messages = [
        HumanMessage(content=input_text)
    ]
    chat_model_res = chat_model.generate([messages])
    output_text = chat_model_res.generations[0][0].text
    return output_text