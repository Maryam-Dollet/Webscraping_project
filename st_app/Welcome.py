import streamlit as st
import plotly.express as px
from cache_func import load_positions, load_results

st.set_page_config(layout="wide")

st.title("Jeux Olympiques une étude de leur croissance et leur effet sur le monde")

results = load_results()

st.dataframe(results)
