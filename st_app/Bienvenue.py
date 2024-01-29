import streamlit as st
import plotly.express as px
from cache_func import load_positions, load_results

st.set_page_config(layout="wide")

st.title("Jeux Olympiques une étude de leur croissance et leur effet sur le monde")

df_city_positions = load_positions()

# st.dataframe(df_city_positions)

fig = px.scatter_geo(
    df_city_positions,
    lat=df_city_positions.latitude,
    lon=df_city_positions.longitude,
    hover_name="description",
)
fig.update_layout(
    width=1000, height=800, title=f"Host Cities of Summer Games across the years"
)
fig.update_geos(
    bgcolor="#0E1117",
    coastlinecolor="#fff",
    lataxis=dict(showgrid=True, gridwidth=0.2),
    lonaxis=dict(showgrid=True, gridwidth=0.2),
    showcountries=True,
)
fig.update_traces(marker_color="#1E90FF", selector=dict(type="scattergeo"))
fig.update_traces(marker_size=8, selector=dict(type="scattergeo"))

st.plotly_chart(fig)