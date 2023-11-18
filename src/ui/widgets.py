import time

import streamlit as st
widget_id = (id for id in range(1, 100_00))


def page_config(title, desc):
    st.markdown(f"# {title}")
    st.sidebar.header(f"{title}")
    st.write(f"{desc}")


def save_button(key, on_click, label='保存'):
    if st.button(key=key, label=label, on_click=on_click):
        st.success(f'{label}成功')


def text_input_group(group_dict: dict, info=None):
    if info:
        st.markdown(info)
    label_map = {
        'prompt': '提示词',
        'speech': '回复话术'
    }
    inputs = {
        label: st.text_input((label_map.get(label) or label), value, key=f'{info}{label}')
        for label, value in group_dict.items()
    }
    return inputs
