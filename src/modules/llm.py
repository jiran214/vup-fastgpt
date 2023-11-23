#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings


import config

gpt_cfg = config.settings.llm_params['base']
gpt_cfg['openai_proxy'] = config.settings.proxy

chat_model = ChatOpenAI(openai_api_key=gpt_cfg['fastgpt_key'], openai_api_base=gpt_cfg['base_url'])
Embedding = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=gpt_cfg['openai_key'], openai_api_base=gpt_cfg['base_url'])

openai_client = OpenAI(api_key=gpt_cfg['fastgpt_key'], base_url=gpt_cfg['base_url'])