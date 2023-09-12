#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 10:42
# @Author  : 雷雨
# @File    : config.py
# @Desc    :
import json
import pathlib


# 基础配置
debug = True
root = pathlib.Path(__file__).parent
log_path = root.parent / 'logs'
static_path = root.parent / 'static'
voice_path = static_path / 'voice'
proxy = None  # eg: http://127.0.0.1:7890
openai_key_list = [
    'xxxx'
]


# json 配置读取
config_path = root.parent / 'config'
react_params = json.loads(open(file=config_path / 'react.json', mode='r').read())
speech_text_params = json.loads(open(file=config_path / 'speech_text.json', mode='r').read())
live_params = json.loads(open(file=config_path / 'live_server.json', mode='r').read())
