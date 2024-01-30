import streamlit as st
import plotly.express as px
from cache_func import load_positions, load_results

st.set_page_config(layout="wide")

st.title("Jeux Olympiques une étude de leur croissance et leur effet sur le monde")

st.markdown("##### Dans le contexte de l’organisation des Jeux Olympiques 2024, imminents, un retour sur l’impact de ces jeux sur les différent(e)s villes et pays s’impose :")
st.markdown("#### Nous pouvons étudier et percevoir ces changements à travers 3 piliers qui se trouvent être ceux du développement durable : \" "+"l’impact économique, écologique et social de ces JOs.")

st.markdown("#### Comment les Jeux Olympiques se sont-ils développés au cours du temps et quels impacts ces développements ont-ils eus sur les pays organisateurs ?")

st.markdown("Afin de répondre à ces questions, nous avons utilisé des données provenant de plusieurs sources :")
st.markdown("Les sports.infos, tableaux des médailles : https://www.les-sports.info/2021-tokyo-jeux-olympiques-d-ete-s16-c0-b0-j0-u323.html")
st.markdown("l’OCDE, émissions de gaz à effet de serre : https://stats.oecd.org/Index.aspx?DataSetCode=air_ghg")
st.markdown("The world Bank, évolution du PIB par pays : https://databank.worldbank.org/reports.aspx?source=2&series=NY.GDP.MKTP.CD&country#")
st.markdown("Olympedia, informations sur les athlètes : https://www.olympedia.org/athletes/1")

# -- A compléter avec les autres sites -- #

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