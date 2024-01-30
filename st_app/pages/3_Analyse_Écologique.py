import streamlit as st
import plotly.express as px
import pandas as pd

from cache_func import load_hosts

hosts = load_hosts()

hosts = hosts[hosts["Annee"] >=1990]
country_list = ["Japan", "Brazil", "United Kingdom", "China (People's Republic of)", "Greece", "Australia", "United States", "Spain"]
hosts["country"] = country_list

GH_emissions = pd.read_csv('data_csv/cp_GH_emissions_final_version.csv')

filtered_gh = GH_emissions[GH_emissions['country'].isin(country_list)]

filtered_gh = filtered_gh.merge(hosts[["country", "Game", "Annee"]], how="left", on="country")

st.header("Analyse Écologique des Jeux Olympiques")

select1 = st.selectbox("Selectionner un pays", country_list)

st.dataframe(filtered_gh[filtered_gh['country'] == select1])

st.write(filtered_gh['sector'].unique().tolist())

test = filtered_gh[filtered_gh['country'] == select1].groupby('year')['GH emissions'].sum().reset_index()

st.dataframe(test)
game_year = int(filtered_gh[filtered_gh['country'] == select1].iloc[0].Annee)

fig = px.line(test,
              x="year",
              y="GH emissions",
              labels={'x': 'Year', 'y': 'GH Emissions'},
              title=f'Evolution of GH emissions in {select1} over the years')
fig.add_vline(x=game_year, line_width=3, line_dash="dash", line_color="pink")

st.plotly_chart(fig)