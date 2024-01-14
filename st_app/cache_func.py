import streamlit as st
import pandas as pd

@st.cache_data
def load_datasets():
    df_events = pd.read_csv("data_csv/events.csv", sep=";")
    return df_events