# Webscraping_project

Etude des Jeux Olympiques sur les 3 pilliers: Economique, Ecologique et Social

## Organisation des fichiers

### data_csv

Contient les datasets utilisés pour l'analyse des données sur les Jeux Olympiques extraites grâce au web scraping

### data_json

Contient le format de données qui ne sont pas faites pour l'analyse, mais qui ont été transformés en format CSV, contient notamment les données sur les jouers extraits du site olympedia.org

### pickles

Contient la traduction en format de dictionnaire des pays et villes.

### players 

Contient les fichiers JSON de joueurs non concaténés. 

### st_app

Contient les fichiers qui permettent de faire fonctionner la web app streamlit

### Notebooks

**maryam_dollet_first_scrap.ipynb** : Notebook qui contient le code de multithreading pour extraire les joueurs sur olympedia, ainsi que leur parsing.

**scrap_gdp.ipynb** : Notebook contenant le code pour extraire le PIB sur le site databank.worldbank.

**guillaume_de_trentinian_olympic_results.ipynb** : Notebook contenant le scraping du site des médailles.

**environmental_impact_olympic_games.ipynb** : Notebook contenant le scraping du site de l'OCDE sur les Gaz à effet de serre. 

**scrap_last_data.ipynb** : Notebook contenant le scraping des données sur les revenus sur la diffusion des JO et le coût des JO.

**event_data_cleaning.ipynb** : Notebook contenant le nettoyage et rajout de colonne du dataset sur les événements des JO.

**events_analysis.ipynb** : Contient l'analyse des événements des JO, et plus précisement l'analyse sociale (Inclusion de Genre et de Pays).

**get_city_positions.ipynb** : Contient les appels d'API pour ajouter des données dans les datasets. 

**gdp_analysis.ipynb** : Contient l'analyse du PIB des pays hôte de JO et les visualisations.

**analysis_on_scraped_data.ipynb** : Contient l'analyse sur le dataset des médailles et l'analyse sur le dataset des GES ainsi que les visualisations qui vont avec. 