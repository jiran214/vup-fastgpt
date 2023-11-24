#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/15 16:50
# @Author  : 雷雨
# @File    : wechat_server.py
# @Desc    : see https://github.com/smallnew666/ChatGPT-Virtual-Live/blob/main/wechat.py
import threading
import time

from playwright.sync_api import sync_playwright

from utils import enums, live_queue


def run(p):
    last_text = None
    browser = p.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.goto('https://channels.weixin.qq.com/login.html')
    page.wait_for_selector("//span[@class='finder-ui-desktop-menu__name']", timeout=150000)
    page.goto('https://channels.weixin.qq.com/platform/live/liveBuild')
    print('wait...')
    page.wait_for_load_state(state="domcontentloaded")
    page.wait_for_timeout(5000)  # 等待1秒加载
    page.wait_for_selector("//span[@class='message-content']")
    assert 'liveBuild' in page.url, '未检测到开播，请重新允许'
    while True:  # 无限循环，伪监听
        time.sleep(2)
        selectors = page.query_selector_all("//div[@class='live-message-item']")

        username = selectors[-1].query_selector("//span[@class='message-username-desc']")
        role = selectors[-1].query_selector("//span[@class='message-type']")
        new_text = selectors[-1].query_selector("//span[@class='message-content']").inner_text()

        username = username and username.inner_text() or "有人"
        if not new_text or new_text.startswith('欢迎'):
            print('暂无消息')
        elif new_text != last_text:
            last_text = new_text
            input_vars = {
                'text': new_text,
                # 'role': role and role.inner_text(),
                'type': enums.LiveInputType.danmu
            }
            print(input_vars)
            live_queue.send(input_vars)


def connect():
    with sync_playwright() as playwright:
        run(playwright)


if __name__ == '__main__':
    t = threading.Thread(target=connect)
    t.start()
    t.join()
