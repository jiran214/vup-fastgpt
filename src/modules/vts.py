#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/13 19:01
# @Author  : 雷雨
# @File    : vts.py
# @Desc    :
import json
import pathlib

import config
from utils import log

plugin_info = {
    "plugin_name": "start pyvts",
    "developer": "Me",
    "authentication_token_path": str(config.config_path / 'token.txt')
}


class VTSOperator:
    def __init__(self, live2D_actions, vts):
        self.live2D_actions = live2D_actions
        self.vts = vts

    @classmethod
    async def init(cls):
        try:
            import pyvts
        except ImportError:
            raise 'Please run pip install pyvts'
        if not pathlib.Path(plugin_info['authentication_token_path']).exists():
            log.info('首次运行，按照提示获取vts令牌')
            return cls.get_token()
        vts = pyvts.vts(plugin_info=plugin_info)
        await vts.connect()
        await vts.read_token()
        await vts.request_authenticate()  # use token
        response_data = await vts.request(vts.vts_request.requestHotKeyList())
        hotkey_list = []
        for hotkey in response_data['data']['availableHotkeys']:
            hotkey_list.append(hotkey['name'])
        log.info(f'vts连接完成-动作:{hotkey_list}')
        return cls(hotkey_list, vts)

    async def play_action(self, action_name: str):
        if action_name not in self.live2D_actions:
            raise ValueError(f'动作不存在：{action_name}')
        send_hotkey_request = self.vts.vts_request.requestTriggerHotKey(action_name)
        await self.vts.request(send_hotkey_request)
        await self.vts.close()

    @classmethod
    async def get_token(cls):
        try:
            import pyvts
        except ImportError:
            raise 'Please run pip install pyvts'
        vts = pyvts.vts(plugin_info=plugin_info)
        try:
            await vts.connect()
        except ConnectionRefusedError:
            raise '请先打开VTS，并打开API开关！'
        log.info('请在live2D VTS弹窗中点击确认！')
        await vts.request_authenticate_token()  # get token
        await vts.write_token()
        await vts.request_authenticate()  # use token

        response_data = await vts.request(vts.vts_request.requestHotKeyList())
        hotkey_list = []
        for hotkey in response_data['data']['availableHotkeys']:
            hotkey_list.append(hotkey['name'])
        log.info('读取到所有模型动作:', hotkey_list)
        return cls(hotkey_list, vts)