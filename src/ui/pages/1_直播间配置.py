"""
{
  "bilibili": {
    "room_id": 510,
    "credential": {
      "sessdata": "0bef7d1b%2C1710091984%2Cdd09c%2A91CjBokNCmTnsRuwrvaU93B188bVqa3hFAu0tu7oefx_7rSWWmjkJo1L0ZKWiV2o2ZvAASVkR4VEpTUzhHNThCTEZmMFBDVXRmQ0tYdzJzaExtZzUyTkotanZmN2VtMUJXdEhKdEQxdHRHOFhKZDV3WlNPS0VyNnNpVWtUejBlTlhyNng0Z1U5eVJnIIEC",
      "bili_jct": "15a331529e1396dc09116f25ad539225",
      "buvid3": "7FBCC946-3762-249F-5F44-A76F1737260657495infoc",
      "dedeuserid": "410282523",
      "ac_time_value": "ee742ca7c376a3faeff6de958d3e4a91"
    },
  },
  "wechat":{},
  "temple":{
    "弹幕": {
      "prompt": "{text}",
      "speech": "{text}。{gpt}"
    },
    "礼物": {
      "prompt": "{text}\n 请表示感谢，说一句赞美他的话！",
      "speech": "{gpt}"
    },
    "sc": {
      "prompt": "{text}",
      "speech": "{text}。{gpt}"
    }
  }
}
"""

import streamlit as st
import config
from ui import widgets, utils

st.session_state.live_server = config.settings.live_params

widgets.page_config('直播间配置', '该页面为B站和视频号回复模板、房间号、认证信息配置')

# 1
st.markdown('## BiliBili服务器')
room_id = st.number_input('房间号', value=int(st.session_state.live_server['bilibili']['room_id']), format='%d')
st.markdown('### 账号认证参数\n每隔一段时间会失效')

st.link_button("浏览器获取认证信息教程", "'https://nemo2011.github.io/bilibili-api/#/get-credential'")
credential_dict = widgets.text_input_group(st.session_state.live_server['bilibili']['credential'])
st.session_state.live_server['bilibili'].update(
    room_id=room_id,
    credential=credential_dict
)
widgets.save_button(
    'save_bilibili',
    on_click=lambda: utils.write_json('live_server.json', st.session_state.live_server)
)

# 2
st.markdown('## 视频号服务器')
st.write('暂无配置')
if st.button(key='save_wechat', label='保存'):
    st.success('暂无配置')

st.markdown("""## 回复模板
- {gpt}为特殊变量，不能修改！
- {text}： text用户输入
- {gpt}： gpt响应结果
""")
context = {'弹幕': widgets.text_input_group(st.session_state.live_server['temple']['弹幕'], '### 弹幕'),
           '礼物': widgets.text_input_group(st.session_state.live_server['temple']['礼物'], '### 礼物'),
           'sc': widgets.text_input_group(st.session_state.live_server['temple']['sc'], '### sc')}

st.session_state.live_server['temple'].update(**context)
widgets.save_button(
    'save_temple',
    on_click=lambda: utils.write_json('live_server.json', st.session_state.live_server)
)


