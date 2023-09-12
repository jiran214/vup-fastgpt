#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 10:40
# @Author  : 雷雨
# @File    : logger.py
# @Desc    :
import sys

from loguru import logger
import config


def get_loguru_logger(file_name):
    """loguru 全局只有一个实例"""
    logger.remove()  # 清除默认配置的处理器和格式器

    logfile = f'{file_name}.log'

    # 添加控制台处理器
    if config.debug:
        logger.add(sys.stdout, level="DEBUG")
    else:
        # 添加文件处理器
        logger.add(config.log_path / logfile, level="INFO", rotation='100 MB')
    return logger
