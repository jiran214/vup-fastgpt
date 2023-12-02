import pandas as pd
import streamlit as st

import config
from ui import widgets, utils


sche_map = {
    'name': '名称',
    'frequency': '循环频率(分钟)',
    'timing': '定时时间',
    'prompt': 'prompt',
    'speech': '回复模板',
    'switch': '是否启用',
}

widgets.page_config('任务配置', """### 任务类型
- 1.定时任务: 在几点几分，做某件事情
- 2.循环任务: 每隔多少时间做某件事
- 3. prompt为空则数字人会说固定的话术，反之会请求GPT""")

st.session_state.scheduler_params = config.settings.scheduler_params
columns = list(sche_map.values())
st.markdown('### 任务面板')
data_df = pd.DataFrame(
    st.session_state.scheduler_params
)

edited_df = st.data_editor(
    data_df,
    column_config={
        'name': st.column_config.Column(
            sche_map['name']
        ),
        "switch": st.column_config.CheckboxColumn(
            "是否启用任务",
        ),
        "prompt": st.column_config.TextColumn(
            "Prompt",
        ),
        'frequency': st.column_config.Column(
            sche_map['frequency']
        ),
        'timing': st.column_config.Column(
            sche_map['timing'],
            help="格式 9:15、21:15"
        ),
        'speech': st.column_config.Column(
            sche_map['speech'],
            help="回复模板"
        ),
    },
    num_rows="dynamic"
)


st.session_state.scheduler_params = edited_df.to_dict(orient='records')
widgets.save_button(key='sche', on_click=lambda: (
    utils.write_json('scheduler.json', data=st.session_state.scheduler_params)
), label='保存任务')
#
# st.markdown('### 添加新任务')
# col1, col2, col3 = st.columns(3)
# task = {
#     'name': col1.text_input('名称'),
#     'frequency': col2.text_input('循环频率(分钟)'),
#     'timing': col3.text_input('定时时间'),
#     'prompt': st.text_area('prompt'),
#     'speech': st.text_input('回复模板'),
#     'switch': True,
# }
# widgets.save_button(key='add', on_click=lambda: (
#     st.session_state.scheduler_params.append(task),
#     utils.write_json('scheduler.json', data=st.session_state.scheduler_params)
# ), label='添加任务')