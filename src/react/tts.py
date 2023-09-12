#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 10:37
# @Author  : 雷雨
# @File    : tts.py
# @Desc    :
"""
 @Author: jiran
 @Email: jiran214@qq.com
 @FileName: audio.py
 @DateTime: 2023/4/24 14:16
 @SoftWare: PyCharm
"""
import asyncio
import threading
import time
from pprint import pprint

import edge_tts
from pygame import mixer, time as pygame_time

import config

audio_lock = threading.Lock()


tts_cfg = config.react_params['tts']
tts_cfg['proxy'] = config.proxy


async def tts_save(text):
    tts = edge_tts.Communicate(text=text, **tts_cfg)
    path = config.voice_path / f"{str(time.time())[:10]}.mp3"
    path = str(path)
    await tts.save(path)
    return path


def play_sound(file_path: str):
    with audio_lock:
        # 播放生成的语音文件
        mixer.init()
        mixer.music.load(file_path)
        mixer.music.play()
        while mixer.music.get_busy():
            pygame_time.Clock().tick(10)

        mixer.music.stop()
        mixer.quit()


def list_voices():
    pprint(asyncio.run(edge_tts.list_voices()))
