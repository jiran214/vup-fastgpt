"""
{
  "base": {
    "base_url": "",
    "proxy": "http://127.0.0.1:7890",
    "openai_key": "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"
  },
  "gpt": {
    "temperature": 0.7,
    "openai_api_base": null,
    "max_retries": 1,
    "max_tokens": 300,
    "openai_organization": null,
    "model_name": "gpt-3.5-turbo"
  },
  "prompt": {
    "system": null
  }
}
"""


import streamlit as st
from ui import vup, widgets, utils

st.session_state.llm_params = vup.settings.llm_params
st.session_state.react_params = vup.settings.react_params

widgets.page_config('虚拟人配置', """## AI虚拟人配置
### AI虚拟人配置 AI引擎(二选一)
- 1.fastgpt: 在fastgpt获取应用key（已经在fastgpt配置好，不需要改动）
- 2.openai: sk-开头的key""")

st.write('修改AI主播配置（Prompt、知识库) 请到：')
st.link_button("前往FastGPT", 'http://ai.newhopedairy.cn/app/detail?appId=6558fcbced049c3059f0e1d8&currentTab=API')

st.session_state.llm_params['base'].update(
    proxy=st.text_input('代理地址', help='访问fastgpt无需配置该项目', key='proxy', value=st.session_state.llm_params['base']['proxy']),
    openai_key=st.text_input('API密钥 / FastGPT密钥', key='openai_key', value=st.session_state.llm_params['base']['openai_key']),
    base_url=st.text_input('fastgpt服务器地址', help='访问openai无需配置该项目', key='base_url', value=st.session_state.llm_params['base']['base_url'])
)
voice = st.selectbox(
   "音色选择，默认女声",
   ("zh-CN-YunxiNeural", "zh-CN-XiaoyiNeural"),
   index=1,
   placeholder="Select voice...",
)
widgets.save_button(
    'save_llm',
    on_click=lambda: (
        utils.write_json('llm.json', st.session_state.llm_params),
        utils.write_json('react.json', st.session_state.react_params)
    )
)



