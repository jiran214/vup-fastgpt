#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/13 19:01
# @Author  : 雷雨
# @File    : vts.py
# @Desc    :
import asyncio
import json
import pathlib
import re
import time

from bilibili_api import sync

import config
from modules.llm import Embedding
from utils import log
from utils.concurrent import Thread

plugin_info = {
    "plugin_name": "start pyvts",
    "developer": "黑小优",
    "authentication_token_path": str(config.config_path / 'token.txt')
}


def get_actions():
    action_list = []
    dir_path = pathlib.Path("C:/Users/jiran/Desktop/黑小优(1)/黑小优")
    for file in dir_path.iterdir():
        if 'exp3.json' in str(file):
            action = json.load(
                fp=open(file=file, mode='r')
            )['Parameters']
            action_id = action[0]['Id']
            action_name = re.search('(.*).exp3.json', file.name).group(1)
            action_list.append({
                'name': action_name,
                'id': action_id,
                'embedding': None
            })
    filename = str(config.config_path / 'action.json')
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(action_list, f, ensure_ascii=True, indent=4)


def embed():
    filename = str(config.config_path / 'action.json')
    actions = json.load(fp=open(file=filename, mode='r', encoding='utf-8'))
    for action in actions:
        action['embedding'] = Embedding.embed_query(action['name'])
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(actions, f, ensure_ascii=False, indent=4)


class VTSOperator:

    @classmethod
    def init(cls, close=False):
        loop = asyncio.get_event_loop()
        vts, hotkey_list = loop.run_until_complete(cls.__init())
        if close:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(vts.close())
        else:
            return vts, hotkey_list

    @classmethod
    async def __init(cls):
        try:
            import pyvts
        except ImportError:
            raise 'Please run pip install pyvts'
        if not pathlib.Path(plugin_info['authentication_token_path']).exists():
            log.info('首次运行，按照提示获取vts令牌')
            return await cls.get_token()
        vts = pyvts.vts(plugin_info=plugin_info)
        await vts.connect()
        await vts.read_token()
        await vts.request_authenticate()  # use token
        response_data = await vts.request(vts.vts_request.requestHotKeyList())
        hotkey_list = []
        if 'errorID' in response_data['data']:
            return await cls.get_token()
        for hotkey in response_data['data']['availableHotkeys']:
            if hotkey['name']:
                hotkey_list.append(hotkey['name'])
        return vts, hotkey_list

    async def _aplay_action(self, action_name: str):
        vts, hotkey_list = await self.__init()
        if action_name not in hotkey_list:
            raise ValueError(f'动作不存在：{action_name}')
        send_hotkey_request = vts.vts_request.requestTriggerHotKey(action_name)
        await vts.request(send_hotkey_request)
        await vts.close()


    @classmethod
    async def get_token(cls):
        try:
            import pyvts
        except ImportError:
            raise 'Please run pip install pyvts'
        vts = pyvts.vts(plugin_info=plugin_info)
        while 1:
            try:
                await vts.connect()
                break
            except Exception as e:
                log.warning(f'未检测到VTS，请打开VTS，并开启API开关！{e}')
                time.sleep(3)
        log.info('请在live2D VTS弹窗中点击确认！')
        await vts.request_authenticate_token()  # get token
        await vts.write_token()
        await vts.request_authenticate()  # use token

        response_data = await vts.request(vts.vts_request.requestHotKeyList())
        hotkey_list = []
        for hotkey in response_data['data']['availableHotkeys']:
            if hotkey['name']:
                hotkey_list.append(hotkey['name'])
        log.info(f'vts连接完成-动作:{hotkey_list}')
        return vts, hotkey_list


if __name__ == '__main__':
    # get_actions()
    # embed()
    vts = VTSOperator.init()
    # actions = ['24小时', '今日', '喝牛奶', '打招呼', '抱牛', '拿牛奶', '换衣服', '文件', '无语', '无辜', '星星眼', '有机', '比心', '活润', '生气', '给牛奶', '脸红', '阴暗', '', '', '']
    # t = Thread(sync(vts._aplay_action(actions[3])))
    # t = Thread(vts.play_action, '打招呼aa')
    # t.join()