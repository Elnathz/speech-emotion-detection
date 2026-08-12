"""Entry point aplikasi Streamlit — konfigurasi global & navigasi antar halaman."""

from __future__ import annotations

import torch
import streamlit as st

from components.css import inject_custom_css
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="Speech Emotion Recognition",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_custom_css()

device_name = "cuda" if torch.cuda.is_available() else "cpu"

pages = [
    st.Page("pages/analisis.py", title="Analisis Emosi", icon="🎙️", default=True),
    st.Page("pages/dashboard.py", title="Dashboard", icon="📊"),
]
pg = st.navigation(pages)
render_sidebar(device_name)
pg.run()
