#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 11:18
# @Author  : 雷雨
# @File    : limit.py
# @Desc    :
import time
import typing
from threading import Lock

from ratelimit import RateLimitDecorator


class KeyManager:
    def __init__(self, api_key_list, sleep_time=2, seconds=3, max_calls=60, callback=None):
        self.lock = Lock()
        self.seconds = seconds
        self.sleep_time = sleep_time
        self.max_calls = max_calls
        self.callback = callback
        self.rate_limiters = {}

        for key in api_key_list:
            self.rate_limiters[key] = RateLimitDecorator(
                calls=max_calls,
                period=seconds,
                raise_on_limit=False,
            )(lambda x: x)

    def assign(self):
        with self.lock:
            while 1:
                for key, rate_limiter in self.rate_limiters.items():
                    if key := rate_limiter(key):
                        return key
                time.sleep(self.sleep_time)
                if self.callback:
                    self.callback()
                else:
                    print('wait')


def inject_param_decorator(**inject_kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 在调用函数之前，注入额外参数
            for kwargs_key, kwargs_value in inject_kwargs.items():
                if isinstance(kwargs_value, typing.Callable):
                    kwargs_value = kwargs_value()
                kwargs[kwargs_key] = kwargs_value
            return func(*args, **kwargs)
        return wrapper
    return decorator