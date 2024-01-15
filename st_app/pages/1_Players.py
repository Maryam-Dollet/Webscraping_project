import streamlit as st
from cache_func import load_datasets

st.set_page_config(layout="wide")

st.title("Etude des joueurs")

events = load_datasets()

st.dataframe(events)