import streamlit as st
import config

md = open(f"{config.root.parent / 'README.md'}", mode='r', encoding='utf-8').read()
st.markdown(md)