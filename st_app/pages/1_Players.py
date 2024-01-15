import streamlit as st
from cache_func import load_events

st.set_page_config(layout="wide")

st.title("Etude des joueurs")

events = load_events()

st.dataframe(events)