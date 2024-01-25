import streamlit as st
import pandas as pd

@st.cache_data
def load_events():
    df_events = pd.read_csv("data_csv/events_cleaned.csv", sep=";")
    games_df = df_events[df_events['season'].isin(["Summer", "Winter"])]
    return games_df

@st.cache_data
def load_results():
    df_results = pd.read_csv("data_csv/results.csv", sep=",")
    return df_results

@st.cache_data
def load_positions():
    df_positions = pd.read_csv("data_csv/host_city_position.csv", sep=",")
    df_results = load_results()

    df_merged = df_results.merge(df_positions, how="left", on="Lieu")
    df_merged["description"] = df_merged["Lieu"].astype(str) + " " + df_merged["Annee"].astype(str)
    df_merged = df_merged.drop_duplicates(subset=["Lieu","Annee"]).sort_values("Annee", ignore_index=True)
    return df_merged[["Lieu", "Annee", "longitude", "latitude", "description"]]