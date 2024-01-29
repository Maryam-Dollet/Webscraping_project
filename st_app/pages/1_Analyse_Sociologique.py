import streamlit as st
import plotly.express as px
from cache_func import load_events

st.set_page_config(layout="wide")

st.title("Etude des joueurs")

events = load_events()

st.dataframe(events)

gender_df = events.drop_duplicates(subset=["id", "year"], ignore_index=True).groupby('year')['Sex'].value_counts().reset_index()

fig = px.bar(
    gender_df,
    x="year",
    y="count",
    color="Sex",
    barmode="group",
    width=1400,
    height=800,
    text_auto=".2s",
)

fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig.update_xaxes(type="category")
fig.update_xaxes(tickangle=45)

st.markdown("#### Répartition des athlètes selon le genre au cours des années")
st.plotly_chart(fig)