import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

from cache_func import load_hosts

hosts = load_hosts()

hosts = hosts[hosts["Annee"] >=1990]
country_list = ["Japan", "Brazil", "United Kingdom", "China (People's Republic of)", "Greece", "Australia", "United States", "Spain"]
hosts["country"] = country_list

GH_emissions = pd.read_csv('data_csv/cp_GH_emissions_final_version.csv')

filtered_gh = GH_emissions[GH_emissions['country'].isin(country_list)]

filtered_gh['GH % augmentation'] = 0

for i in range(len(filtered_gh)):
    # if the year is 1990, we replace the value of the column 'GH % augmentation' by 0
    # we have sector, countryn year, GH % augmentation
    if filtered_gh.iloc[i, 2] == 1990:
        filtered_gh.iloc[i, 4] = np.nan
    # if the year is not 1990, we compute the % of augmentation of GH emissions compared to the previous year
    else:
        # we search the value of the previous year
        previous_year = filtered_gh.iloc[i, 2] - 1
        # we search the value of GH emissions of the previous year
        previous_year_GH = filtered_gh[(filtered_gh['sector'] == filtered_gh.iloc[i, 0]) & (filtered_gh['country'] == filtered_gh.iloc[i, 1]) & (filtered_gh['year'] == previous_year)]['GH emissions'].values[0]
        # if previous_year_GH is nan or aumgentation.iloc[i, 3] is a nan value, we replace the value of the column 'GH % augmentation' by nan
        if np.isnan(previous_year_GH) or np.isnan(filtered_gh.iloc[i, 3]):
            filtered_gh.iloc[i, 4] = np.nan
        else:
            # we compute the % of augmentation of GH emissions compared to the previous year
            filtered_gh.iloc[i, 4] = (filtered_gh.iloc[i, 3] - previous_year_GH) / previous_year_GH * 100

filtered_gh = filtered_gh.merge(hosts[["country", "Game", "Annee"]], how="left", on="country")

st.header("Analyse Écologique des Jeux Olympiques")

select1 = st.selectbox("Selectionner un pays", country_list)

with st.expander("Raw Data"):
    st.dataframe(filtered_gh[filtered_gh['country'] == select1])

st.markdown("#### Available Sectors of the GH emissions")
st.write(filtered_gh['sector'].unique().tolist())

test = filtered_gh[filtered_gh['country'] == select1].groupby('year')['GH emissions'].sum().reset_index()

# st.dataframe(test)
game_year = int(filtered_gh[filtered_gh['country'] == select1].iloc[0].Annee)

fig = px.line(test,
              x="year",
              y="GH emissions",
              labels={'x': 'Year', 'y': 'GH Emissions'},
              title=f'Evolution of GH emissions in {select1} over the years', 
              height=600,
              width=1000)
fig.add_vline(x=game_year, line_width=3, line_dash="dash", line_color="pink")

st.plotly_chart(fig)

fig = px.line(filtered_gh[filtered_gh['country'] == select1].groupby(['year', 'sector'])['GH % augmentation'].sum().reset_index(),
              x='year',
              y='GH % augmentation',
              color='sector',
              labels={'x': 'Year', 'y': 'GH % Augmentation'},
              height=800,
              width=1200)
fig.update_layout(title_text=f'Evolution of GH emissions % of augmentation in {select1} over the years by sector')
fig.add_vline(x=game_year, line_width=3, line_dash="dash", line_color="pink")

st.plotly_chart(fig)


st.markdown(f"##### {select1} a accueilli les jeux olympiques en {game_year}")

st.markdown(f"Après une étude approfondie; chez les pays organisateurs, nous avons pu voir des changements significatifs dans les émissions de GES les années des JO
             pour certains secteurs d'émission. Cependant, cela ne peut pas être directement attribué aux jeux olympiques."
            +" Les émissions de ces secteurs d'activité sont trop fluctuantes pour que nous puissions tirer une conclusion tranchée de cette analyse.")

st.markdown("Pour conclure, nous pouvons dire que nous n'avons pas relevé d'impact significatif des jeux olympiques sur les émissions de GES du pays hôte d'une année à l'autre."
            +" Nous sommes limités par nos données en ce sens. Nous pourrions potentiellement obtenir des résultats plus probants en étudiant les émissions de GES uniquement de la ville hôte et non du pays entier."
            +" De telles données sont difficilement accessibles mais obtenir des données mensuelles ou hebdomadaires serait également plus probant")