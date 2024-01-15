#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/13 19:01
# @Author  : 雷雨
# @File    : vts.py
# @Desc    :
import threading
import time
from typing import Optional

import pyvts
from bilibili_api import sync
import sys
# sys.path.insert(0, 'D:/project/gpt/vup-fastgpt/src')

import config
from utils import log

plugin_info = {
    "plugin_name": "start pyvts",
    "developer": "黑小优",
    "authentication_token_path": str(config.config_path / 'token.txt')
}


class VTSOperator:

    def __init__(self):
        try:
            import pyvts
        except ImportError:
            raise 'Please run pip install pyvts'
        self.hotkey_list = None
        self.vts: Optional[pyvts.vts] = pyvts.vts(plugin_info=plugin_info)

    @classmethod
    async def init(cls):
        instance = cls()
        await instance.ainit()
        return instance

    async def ainit(self):
        log.info('请在live2D VTS弹窗中点击确认！')
        while 1:
            try:
                await self.vts.connect()
                assert self.vts.get_connection_status() == 1, '连接异常'
                await self.vts.request_authenticate_token()  # get token
                assert await self.vts.request_authenticate()  # use token
                break
            except Exception as e:
                log.warning(f'未检测到VTS连接，请打开VTS，并开启API开关！{e}')
                time.sleep(3)
        await self.vts.write_token()
        self.hotkey_list = await self.get_hotkey_list()
        assert self.hotkey_list, '获取模型动作失败'
        await self.vts.close()

    async def _aplay_action(self, action_name: str):
        try:
            # self.vts = pyvts.vts(plugin_info=plugin_info)
            # await self.vts.read_token()
            await self.vts.connect()
            assert self.vts.get_connection_status() == 1, '连接失败'
            assert await self.vts.request_authenticate(), 'VTS连接异常-认证失败'
            if action_name not in self.hotkey_list:
                raise ValueError(f'动作不存在：{action_name}')
            send_hotkey_request = self.vts.vts_request.requestTriggerHotKey(action_name)
            await self.vts.request(send_hotkey_request)
            log.info('播放动作结束')
            await self.vts.close()
        except Exception as e:
            log.error(f'播放动作异常')
            print('异常信息:', e)

    async def get_hotkey_list(self):
        response_data = await self.vts.request(self.vts.vts_request.requestHotKeyList())
        hotkey_list = []
        for hotkey in response_data['data']['availableHotkeys']:
            if hotkey['name']:
                hotkey_list.append(hotkey['name'])
        log.info(f'vts连接完成-动作:{hotkey_list}')
        return hotkey_list


async def test_vts():
    vts_opt = VTSOperator()
    await vts_opt.ainit()
    for _ in range(6 * 100):
        await vts_opt._aplay_action('喝牛奶')
        time.sleep(10)
        print('测试正常')


if __name__ == '__main__':
    sync(test_vts())