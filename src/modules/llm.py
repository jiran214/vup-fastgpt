#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/14 11:41
# @Author  : 雷雨
# @File    : llm.py
# @Desc    :
import openai
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

import config
from utils.limit import KeyManager, inject_param_decorator

gpt_cfg = config.llm_params['gpt']
gpt_cfg['openai_proxy'] = config.proxy


key_manager = KeyManager([key for key in config.openai_key_list if key])
openai.ChatCompletion.create = inject_param_decorator(api_key=key_manager.assign)(openai.ChatCompletion.create)
openai.Embedding.create = inject_param_decorator(api_key=key_manager.assign)(openai.Embedding.create)
chat_model = ChatOpenAI(**gpt_cfg, openai_api_key='temp')
Embedding = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key='temp')