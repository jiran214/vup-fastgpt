#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 10:42
# @Author  : 雷雨
# @File    : config.py
# @Desc    :
import json
import os
import pathlib

import openai

# 基础配置
debug = True
root = pathlib.Path(__file__).parent
log_path = root.parent / 'logs'
static_path = root.parent / 'static'
voice_path = static_path / 'voice'
config_path = root.parent / 'config'


# 文件配置读取
react_params = json.loads(open(file=config_path / 'react.json', mode='r').read())
llm_params = json.loads(open(file=config_path / 'llm.json', mode='r').read())
live_params = json.loads(open(file=config_path / 'live_server.json', encoding='utf-8', mode='r').read())
scheduler_params = json.loads(open(file=config_path / 'scheduler.json', encoding='utf-8', mode='r').read())
filter_words = [line.strip() for line in open(file=config_path / 'filter_words.txt', encoding='utf-8', mode='r').readlines()]


# 初始化配置
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ''
proxy = llm_params['base']['proxy']  # eg: http://127.0.0.1:7890
openai_key_list = llm_params['base']['openai_key_list']
if proxy:
    os.environ['HTTPS_PORXY'] = proxy
    os.environ['HTTP_PORXY'] = proxy
    openai.proxy = proxy


# 功能选项
action = False