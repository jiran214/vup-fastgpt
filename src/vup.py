#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 11:06
# @Author  : 雷雨
# @File    : brain.py
# @Desc    :
from bilibili_api import sync
from langchain.schema import SystemMessage, HumanMessage
from utils.utils import top_n_indices_from_embeddings

from modules import tts, llm
from modules.vts import VTSOperator


class Brain:
    def think(self, input_text):
        # 使用Fastgpt不需要 SystemMessage(content="...", additional_kwargs={}),
        messages = [
            HumanMessage(content=input_text)
        ]
        chat_model_res = llm.chat_model.generate([messages])
        output_text = chat_model_res.generations[0][0].text
        return output_text


class Mouth:
    def speak(self, speech_text):
        path = sync(tts.tts_save(speech_text))
        tts.play_sound(path)


class Body:

    def __init__(self, vts_opt: VTSOperator):
        self.live2D_actions = vts_opt.live2D_actions
        self.live2D_embeddings = llm.Embedding.aembed_documents(texts=vts_opt.live2D_actions)
        self.vts_opt = vts_opt

    def feel(self, input_text):
        txt_embedding = llm.Embedding.embed_query(input_text)
        action_name = self.live2D_actions[
            int(top_n_indices_from_embeddings(txt_embedding, self.live2D_embeddings, top=1)[0])
        ]
        return action_name

    def action(self, action_name):
        sync(self.vts_opt.play_action(action_name))


class VTuber:
    def __init__(self, vts_opt):
        self.brain = Brain()
        self.mouth = Mouth()
        self.body = Body(vts_opt)
