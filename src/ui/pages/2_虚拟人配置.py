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
import os

import streamlit as st

from ui import widgets, utils
import config

st.session_state.llm_params = config.settings.llm_params
st.session_state.react_params = config.settings.react_params

widgets.page_config('虚拟人配置', """### AI虚拟人配置 AI引擎(二选一)
不需要修改太多，更新词库就行
- 1.fastgpt: 在fastgpt获取应用key
- 2.openai: sk-开头的key""")

st.write('修改（Prompt、知识库) 请到FastGPT')
cols = st.columns(2)

cols[0].write('修改（Prompt、知识库) 请到FastGPT')
cols[1].link_button("前往FastGPT配置AI主播", 'http://ai.newhopedairy.cn/app/detail?appId=6558fcbced049c3059f0e1d8')

widgets.save_button(
    key='open_file',
    on_click=lambda: os.startfile(f'{config.config_path / "filter_words.txt"}', operation='open'),
    label='打开敏感词库'
)

st.session_state.llm_params['base'].update(
    proxy=st.text_input('代理地址', help='访问fastgpt无需配置该项目', key='proxy', value=st.session_state.llm_params['base']['proxy']),
    openai_key=st.text_input('OPENAI密钥', key='openai_key', value=st.session_state.llm_params['base']['openai_key']),
    fastgpt_key=st.text_input('FastGPT密钥', key='fastgpt_key', value=st.session_state.llm_params['base']['fastgpt_key']),
    base_url=st.text_input('fastgpt服务器地址', help='访问openai无需配置该项目', key='base_url', value=st.session_state.llm_params['base']['base_url'])
)

st.session_state.react_params['tts']['voice'] = st.selectbox(
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



