import collections
import pathlib
import sys


sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))


from ui import widgets
import streamlit as st
import apis


import config
settings = config.settings

style = "<style>h1, h2 {text-align: center;}</style>"
st.markdown(style, unsafe_allow_html=True)
widgets.page_config('FastGPT-VUP', """## 新希望乳业 FastGPT-VUP AI数字
请提前准备
- 打开VBCABLE_C虚拟声卡，并设置好VTS/OBS/本机音源输入、输出
- 打开VTS 并已经完成验证""")


str_output = st.empty()


cols = st.columns(4)

st.write('请打开VTS APis开关,开播后在VTS弹出框点击确认连接')
if cols[1].button(key='run_bilibili', label='启动Bilibili直播', on_click=lambda: apis.start('bilibili')):
    st.success(f'启动中')

if cols[2].button(key='run_wechat', label='启动视频号直播', on_click=lambda: apis.start('wechat')):
    st.success(f'启动中，请在弹出的浏览器扫码登录视频号后台，扫码后将网页最小化，请勿有多余操作')

if apis.p:
    if cols[3].button(key='over_process', label='结束进程', on_click=apis.stop, type="primary"):
        st.success(f'结束进程成功')
