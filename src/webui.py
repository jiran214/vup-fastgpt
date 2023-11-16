#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gradio as gr
import os

gr.State()


class State:
    def __init__(self):
        self.a = gr.State('1')
        self.b = gr.State('2')
        self.choices = ['1', '2']

    def get(self, key):
        return lambda: getattr(self, key)

    def combine(self, a, b):
        self.a = self.a + self.b
        self.b = self.b + self.a
        s.choices.append(self.a)
        return self.a, self.b, 'True'


s = State()


with gr.Blocks() as demo:
    txt = gr.Textbox(label="Input", lines=2, value=s.get('a'))
    txt_2 = gr.Textbox(label="Input 2", value=s.get('b'))
    txt_3 = gr.Textbox(value="", label="Output")
    txt_4 = gr.Radio(choices=s.choices, label="Output")
    txt_5 = gr.Dropdown(choices=s.choices, label="Output")
    btn = gr.Button(value="Submit")
    btn.click(s.combine, inputs=[txt, txt_2], outputs=[txt, txt_2, txt_3])


if __name__ == "__main__":
    demo.launch()

