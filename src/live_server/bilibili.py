#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 11:38
# @Author  : 雷雨
# @File    : bilibili.py
# @Desc    :
from bilibili_api import sync
from utils import enums, live_queue


def on_danmaku(event_dict):
    input_vars = {
        'text': event_dict['data']['info'][1],
        'user_name': event_dict['data']['info'][2][1],
        'time': event_dict['data']['info'][9]['ts'],
        'type': enums.LiveInputType.danmu
    }
    live_queue.send(input_vars)


def on_gift(event_dict):
    info = event_dict['data']['data']
    input_vars = {
        'user_name': info['uname'],
        'face': info['face'],
        'action': info['action'],
        'giftName': info['giftName'],
        'time': info['timestamp'],
        'type': enums.LiveInputType.gift
    }
    input_vars['text'] = f"{input_vars['user_name']}{input_vars['action']}了{input_vars['giftName']}给你。"
    live_queue.send(input_vars)


def on_super_chat(event_dict):
    info = event_dict['data']['data']
    user_info = info['user_info']
    input_vars = {
        'user_name': user_info['uname'],
        'face': user_info['face'],
        'text': info['message'],
        'price': info['price'],
        'time': info['start_time'],
        'type': enums.LiveInputType.sc
    }
    live_queue.send(input_vars)


class BlLiveRoom:
    def __init__(self, room_id):
        try:
            from bilibili_api import live, sync
        except ImportError:
            raise 'Please run pip install bilibili-api-python'
        self.room = live.LiveDanmaku(room_id)
        self.add_event_listeners()

    def add_event_listeners(self):
        listener_map = {
            'DANMU_MSG': on_danmaku,
            'SEND_GIFT': on_gift,
            'SUPER_CHAT_MESSAGE': on_super_chat,
            'INTERACT_WORD': lambda event_dict: None,
        }
        for item in listener_map.items():
            self.room.add_event_listener(*item)

    def connect(self):
        sync(self.room.connect())