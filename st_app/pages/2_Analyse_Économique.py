import streamlit as st
import plotly.express as px
import pandas as pd
from cache_func import load_gdp, load_hosts

st.title("Analyse Economique des Pays Hôtes")

st.write("Dans cette partie, nous tentons de réaliser une étude du profit des pays qui ont organisés les Jeux Olympiques. Nous avons extrait les PIB de tous les pays du monde sur le site : https://databank.worldbank.org/reports.aspx?source=2&series=NY.GDP.MKTP.CD&country#")

st.write("")

df_gdp = load_gdp()
hosts = load_hosts()

# st.dataframe(df_gdp)

gdp_countries = pd.read_csv("data_csv/country_gdp.csv", sep=";")
# st.dataframe(gdp_countries)
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
    title="Evolution du PIB des Pays (1960-2022)",
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

# st.dataframe(hosts)

st.subheader("Evolution du PIB du pays hôte après les Jeux Olypiques")

st.markdown("On peut ici sélectionner l'année des Jeux Olympiques et voir le PIB 7 ans après pour voir s'il y a eu un impact positif ou négatif.")

select1 = st.selectbox("Select the Game", list(hosts["Game"]))

filtered = hosts[hosts["Game"] == select1][["Game", "iso2", "Annee"]].merge(gdp_countries, how="left", on="iso2").melt(id_vars=["Game", "Annee","country_name", "iso2"], var_name="Year", value_name="GDP")
filtered.Year =  filtered.Year.astype(int)

gap = filtered.iloc[0].Annee
final_filtered = filtered[filtered["Year"].between(gap - 2, gap + 7)]
final_filtered["pct_change"] = final_filtered["GDP"].pct_change() * 100
final_filtered = final_filtered.fillna(0)

st.dataframe(final_filtered.style.format({"Year": lambda x: "{:}".format(x), "Annee": lambda x: "{:}".format(x)}))

fig = px.line(final_filtered, x="Year", y="GDP")
fig.add_vline(x=gap, line_width=3, line_dash="dash", line_color="pink")

st.plotly_chart(fig)

st.markdown("Dans notre cas, on peut voir une croissance varié selon l'année des JO. On ne peut pas simplement dire que ce sont principalement les JO qui ont causé un croissance ou décroissance du PIB, sachant que dans les années 1990 c'était le début de la mondialisation, plusieurs facteurs peuvent faire partie de la raison de pourquoi un tel pays à pu croître économiquement. Mais on peut émettre une hypothèse.")

broadcast_revenue_df = pd.read_csv("data_csv/broadcast_revenue.csv", sep=";")
og_cost_df = pd.read_csv("data_csv/olympic_games_cost.csv", sep=";")

broadcast_revenue_df["revenue"] = broadcast_revenue_df["revenue"].str.replace("$", "")
og_cost_df["Cost"] = og_cost_df["Cost"].str.replace("$", "")

broadcast_revenue_df["revenue"] = (broadcast_revenue_df["revenue"].replace(r'[KMB]+$', '', regex=True).astype(float) * broadcast_revenue_df["revenue"].str.extract(r'[\d\.]+([KMB]+)', expand=False).fillna(1).replace(['K','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
og_cost_df["Cost"] = (og_cost_df["Cost"].replace(r'[KMB]+$', '', regex=True).astype(float) * og_cost_df["Cost"].str.extract(r'[\d\.]+([KMB]+)', expand=False).fillna(1).replace(['K','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
broadcast_revenue_df["desc"] = (broadcast_revenue_df["Year"].astype(str) + " " + broadcast_revenue_df["City"].astype(str) + " " + broadcast_revenue_df["Game_type"].astype(str)).str.replace("nan ", "").str.replace(".0", "")
og_cost_df["desc"] = (og_cost_df["Year"].astype(str) + " " + og_cost_df["City"].astype(str) + " " + og_cost_df["Game_type"].astype(str)).str.replace('nan ', "")

st.markdown("#### Revenus sur la Diffusion des Jeux Olympiques")
# st.dataframe(broadcast_revenue_df.style.format({"Year": lambda x: "{:}".format(x)}))

fig = px.bar(broadcast_revenue_df[["revenue", "desc"]][::-1], x="revenue", y="desc", text_auto='.2s', height=800, width=1000)
st.plotly_chart(fig)

st.markdown("Les jeux olympiques sont de plus en plus diffusés dans le monde entier. Les revenus de la diffusion des jeux olympiques sont donc de plus en plus importants."+
            " On observe également que les jeux d'été sont plus diffusés que les jeux d'hiver et rapportent donc plus de revenus.")

st.markdown("#### Coût des Jeux Olympiques")
# st.dataframe(og_cost_df.style.format({"Year": lambda x: "{:}".format(x)}))

fig = px.bar(og_cost_df[::-1], x="Cost", y="desc", text_auto='.2s', height=600, width=800)
st.plotly_chart(fig)

st.markdown("Nous pouvons observer une totale décorrélation entre la saison des jeux olympiques et leur coût.")

# participation de la diffusion des jeux olympiques à la compensation des coûts (revenu / coût) 
# on ne peut avoir ce pourcentage que pour les années présentes dans les deux dataframes

st.markdown("#### Pourcentage des coûts des jeux olympiques compensés par la diffusion des jeux olympiques")
st.markdown("On ne peut avoir ce pourcentage que pour les années présentes dans les deux dataframes")

merged = broadcast_revenue_df.merge(og_cost_df, how="inner", on=["Year", "City", "Game_type"])
merged["percentage"] = merged["revenue"] / merged["Cost"] * 100
merged["desc"] = (merged["Year"].astype(str) + " " + merged["City"].astype(str) + " " + merged["Game_type"].astype(str)).str.replace('nan ', "")
# st.dataframe(merged.style.format({"Year": lambda x: "{:}".format(x)}))

fig = px.bar(merged[["percentage", "desc"]][::-1], x="percentage", y="desc", color="percentage", text_auto='.2s', height=800, width=1000, color_continuous_scale="purd")
st.plotly_chart(fig)

st.markdown("La part de compensation des coûts des JOs par les revenus provenant de leur diffusion est très variable d'une édition à l'autre :")
st.markdown("Cette diffusion, bien que ne permettant pas de compenser les coûts de l'évènement, y participe tout de même de manière significative !")