import streamlit as st
import plotly.express as px
import pandas as pd
from cache_func import load_events, load_medals

st.set_page_config(layout="wide")

st.title("Etude des joueurs")

events = load_events()

with st.expander("Raw Data"):
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

st.write("On peut remarquer qu'au fil du temps, la parité devient de plus en plus proche, ce qui donne la preuve d'une certaine évolution. Cependant, il y a toujours moins de femme athlètes que d'hommes athlètes, cela peut notamment s'expliquer sur l'écart de financement. En effet les athlètes qui participent dans la catégorie des femmes gagnent moins de le sport que la gente masculine, elles sont également moins financées et rencontrent des problèmes liés à cela.")

st.markdown("#### Pays Participants aux Jeux Olympiques")

noc_df = events.drop_duplicates(subset=["id", "year"]).groupby(by=["year", "NOC"])['NOC'].value_counts().reset_index()
nb_noc = noc_df["year"].value_counts().reset_index().sort_values("year", ignore_index=True)
nb_noc["year"] = nb_noc["year"].astype(str)

fig = px.bar(nb_noc, x="year", y="count", height=600, width=1200, title="Nombre de Pays participant aux JO à travers le temps")
st.plotly_chart(fig)

st.write("Ce graphique montre que de plus en plus de pays participent au cours du temps, on peut dire que les JO deviennent de plus en plus inclusifs.")

st.markdown("#### Nombre de Joueurs par Pays")
year = st.select_slider(
    "Selectionnez l'Année", options=noc_df.sort_values("year").year.unique()
)

filtered_noc = noc_df[noc_df["year"] == year].sort_values("count")

# st.dataframe(filtered_noc)

fig = px.bar(filtered_noc, x='NOC', y="count", height=800, width=1100, title=f"Nombre de Joueur par Pays aux Jeux Olympiques de {year}")
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig)

st.write("Selon ce Grphique, on peut voir qu'au cours du temps les pays augmentent, mais on constate que ce sont les pays les plus développés et avec un PIB élevé qui ont le plus de participants")

st.markdown("#### Analyse des obtentions des médailles")

medals = load_medals()
# st.dataframe(medals)

# on a bar chart px countries in the x axis and total medals in the y axis
fig = px.bar(medals.groupby('Country')['Total'].sum().sort_values(ascending=False).head(10),
             x=medals.groupby('Country')['Total'].sum().sort_values(ascending=False).head(10).index,
             y=medals.groupby('Country')['Total'].sum().sort_values(ascending=False).head(10).values,
             labels={'x': 'Country', 'y': 'Total Medals'}, 
             width=800,
             height=600)
st.plotly_chart(fig)

fig = px.line(medals.groupby('Year')['Total'].sum(),
              x=medals.groupby('Year')['Total'].sum().index,
              y=medals.groupby('Year')['Total'].sum().values,
              labels={'x': 'Year', 'y': 'Total Medals'},
              title='Evolution of total medals distributed over the years',
              width=800,
              height=600)
st.plotly_chart(fig)

fig = px.scatter(medals.groupby(['Year', 'Country'])['Total'].sum().reset_index(),
                 x='Year',
                 y='Total',
                 size='Total',
                 color='Country',
                 labels={'x': 'Year', 'y': 'Total Medals'},
                 title='Evolution of total medals won by each country over the years',
                 width=1200,
                 height=600)
st.plotly_chart(fig)

medals_by_country = medals.groupby('Country').sum()[['Gold', 'Silver', 'Bronze', 'Total']]

fig = px.bar(medals_by_country, x=medals_by_country.index, y=['Gold', 'Silver', 'Bronze'],
             color_discrete_map={'Gold': 'gold', 'Silver': 'silver', 'Bronze': 'brown'},
             title='Medals Distribution by Country',
             labels={'value': 'Number of Medals', 'variable': 'Medal Type'},
             barmode='group',
             width=1200,
             height=600)
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig)

fig = px.bar(medals_by_country.sort_values('Total', ascending=False).head(10),
             x=medals_by_country.sort_values('Total', ascending=False).head(10).index,
             y=['Gold', 'Silver', 'Bronze'],
             color_discrete_map={'Gold': 'gold', 'Silver': 'silver', 'Bronze': 'brown'},
             title='Top 10 Countries - Medals Distribution',
             labels={'value': 'Number of Medals', 'variable': 'Medal Type'},
             barmode='group',
             width=1000,
             height=600)
fig.update_xaxes(title_text='Country')
st.plotly_chart(fig)

fig = px.line(medals[medals['Country'] == 'France'].groupby('Year')['Total'].sum(),
              x=medals[medals['Country'] == 'France'].groupby('Year')['Total'].sum().index,
              y=medals[medals['Country'] == 'France'].groupby('Year')['Total'].sum().values,
              labels={'x': 'Year', 'y': 'Total Medals'},
              title='Evolution of total medals won by France over the years',
              width=1000,
              height=600)
st.plotly_chart(fig)

st.markdown("#### Analyse Historique")
fig = px.scatter(medals[medals['Country'] == 'UNITED STATES'].groupby('Year')['Total'].sum(),
              x=medals[medals['Country'] == 'UNITED STATES'].groupby('Year')['Total'].sum().index,
              y=medals[medals['Country'] == 'UNITED STATES'].groupby('Year')['Total'].sum().values,
              labels={'x': 'Year', 'y': 'Total Medals'},
              title='Evolution of total medals won by the United States over the years',
              width=1000,
              height=600)
st.plotly_chart(fig)

fig = px.scatter(medals[medals['Country'] == 'U.S.S.R.'].groupby('Year')['Total'].sum(),
              x=medals[medals['Country'] == 'U.S.S.R.'].groupby('Year')['Total'].sum().index,
              y=medals[medals['Country'] == 'U.S.S.R.'].groupby('Year')['Total'].sum().values,
              labels={'x': 'Year', 'y': 'Total Medals'},
              title='Evolution of total medals won by the U.S.S.R. over the years',
              width=1000,
              height=600)
st.plotly_chart(fig)