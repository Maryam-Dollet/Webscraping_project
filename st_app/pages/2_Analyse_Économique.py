import streamlit as st
import plotly.express as px
import pandas as pd
from cache_func import load_gdp

st.title("Analyse Economique des Pays Hôtes")

st.write("Dans cette partie, nous tentons de réaliser une étude du profit des pays qui ont organisés les Jeux Olympiques. Nous avons extrait les PIB de tous les pays du monde sur le site : https://databank.worldbank.org/reports.aspx?source=2&series=NY.GDP.MKTP.CD&country#")

st.write("")

df_gdp = load_gdp()

# st.dataframe(df_gdp)

gdp_countries = pd.read_csv("data_csv/country_gdp.csv", sep=";")
st.dataframe(gdp_countries)

gdp_coutries_transposed = gdp_countries.melt(id_vars=["country_name", "iso2"], var_name="Year", value_name="GDP")
# st.dataframe(gdp_coutries_transposed)

# positions = pd.read_csv("data_csv/gdp_country_positions.csv", sep=";")
# st.dataframe(positions)

fig = px.choropleth(
    gdp_coutries_transposed,
    locations="country_name",
    color="GDP",
    hover_name="country_name",
    animation_frame="Year",
    title="",
    color_continuous_scale="deep",
    locationmode="country names",
    width=1200,
    height=800,
)

fig.update_geos(
    lataxis=dict(showgrid=True, gridwidth=0.2, griddash="solid", gridcolor="#000"),
    lonaxis=dict(showgrid=True, gridwidth=0.2, griddash="solid", gridcolor="#000"),
    showcountries=True,
    countrycolor="#999",
)

st.plotly_chart(fig)