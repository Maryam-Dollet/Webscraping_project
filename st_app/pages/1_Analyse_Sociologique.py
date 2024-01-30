import streamlit as st
import plotly.express as px
import pandas as pd
from cache_func import load_events, load_medals

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

st.markdown("#### Pays Participants aux Jeux Olympiques")

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