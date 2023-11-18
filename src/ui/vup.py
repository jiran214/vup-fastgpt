import pathlib
import sys
import time
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))


from ui import widgets
import streamlit as st


# print(111, str(pathlib.Path(__file__).parent.parent))
import config

settings = config.Settings()

style = "<style>h1, h2 {text-align: center;}</style>"
st.markdown(style, unsafe_allow_html=True)
widgets.page_config('FastGPT-VUP', """## 新希望乳业 FastGPT-VUP AI数字人""")
cols = st.columns(8)

if cols[3].button(key='test', label='测试', on_click=lambda: print(1)):
    st.success(f'测试成功')

if cols[4].button(key='run', label='启动', on_click=lambda: print(1)):
    st.success(f'启动成功')


with st.empty():
    st.success("✔️ 1 minute over!")


with st.empty():
    for seconds in range(60):
        st.error(f"⏳ {seconds} seconds have passed")
        time.sleep(1)
    st.write("✔️ 1 minute over!")