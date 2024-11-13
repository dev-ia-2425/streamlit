import streamlit as st
import pandas as pd
from numpy import sort


#### CONFIGURATION


# Configuration du layout
st.set_page_config( layout="wide" )

# Obtention du dataset
source = pd.read_csv("car_prices_clean.csv", encoding='utf-8', delimiter=",")    # Lecture du dataset
df = source
df["saledate"] = pd.to_datetime(df["saledate"], format="mixed").dt.date          # Conversion du type des dates

columns = df.columns                                                       # Nom des colonnes

brands = df["make"].unique()                                               # Marques

models = df["model"].unique()                                              # Modèles

min_price = df["sellingprice"].min()                                       # Prix minimum
max_price = df["sellingprice"].max()                                       # Prix maximum
mid_price = (max_price - min_price) / 2                                    # Prix à mi-chemin

first_date = df["saledate"].min()                                          # Date de vente la plus anciene
last_date = df["saledate"].max()                                           # Date de vente la plus récente

#### INPUTS 


### TITRE - Tri

st.sidebar.markdown("# Trier les lignes")

# Choisir la colonne de tri
order_by = st.sidebar.selectbox(
   "Trier sur cette colonne", 
   columns, 
   index=None, 
   placeholder="Choisir une colonne"
)

# Choisir le type de tri
order = ("Croissant" == (st.sidebar.selectbox("Type de tri", ["Croissant", "Décroissant"])))


### TITRE - Filtres

st.sidebar.markdown("# Filtrer les lignes")

## Custom

# Boite à filtres perso
filter_container = st.sidebar.container()

# Choisir une colonne de filtre
custom_filter = filter_container.multiselect(
   "Ajouter un filtre",
   columns,
   placeholder="Choisir une colonne"
)

## Dates des voitures

# Layout des inputs (côte à côte)
col_date_1, col_date_2 = st.sidebar.columns(2)

# Choisir la date de début
date_first = col_date_1.date_input(
   "Vente après le : ",
   value = first_date,
   min_value = first_date, 
   max_value = last_date  
)

# Choisir la date de fin
date_last = col_date_2.date_input(
   "Vente avant le : ",
   value = last_date,
   min_value = date_first, 
   max_value = last_date
)

## Marque

# Choisir la marque à afficher
make = st.sidebar.selectbox("Marque du véhicule", brands, index=None, placeholder="Choisir une marque")

## Modèle 

# Enlèver les modèles qui ne sont pas d'une marque si elle est sélectionnée  
if(make):
   models = df[df["make"] == make]["model"].unique()

# Choisir le modèle à afficher
model = st.sidebar.selectbox("Modèle du véhicule", models, index=None, placeholder="Choisir un modèle")

## Prix de vente

# Choisir la fourchette de prix à afficher
prices = st.sidebar.slider("Prix de vente", min_price, max_price, (min_price, max_price))

### TITRE - Groupage

st.sidebar.markdown("# Grouper par")

# Choisir une colonne de groupes
group_by = st.sidebar.selectbox(
   "Regrouper en fonction de",
   columns,
   index = None,
   placeholder = "Choisir une colonne"
)

# Fonctions d'aggrégation 

def first(serie):
   uniques = serie.unique()
   uniques = sort(uniques)

   res = str(uniques[0])
   return res

def summary(serie):
   uniques = serie.unique()
   uniques = sort(uniques)

   if len(uniques) > 1:
      res = str(uniques[0]) + ", ..., " + str(uniques[-1])
   else:
      res = str(uniques[0])
   
   return res

def all(serie):
    uniques = serie.unique()
    uniques = sort(uniques)

    res = str(uniques)
    return res

# Dictionnaire des fonctions d'aggrégation

num_functions = {
   "Min":(lambda x: x.min()),
   "Max":(lambda x: x.max()),
   "Moyenne":(lambda x: x.mean()),
   "Médiane":(lambda x: x.median())
}

str_functions = {
   "Premier": (lambda x: x.agg(func=first)),
   "Résumé": (lambda x: x.agg(func=summary)),
   "Tout": (lambda x: x.agg(func=all))
}

# st.sidebar.markdown("#### Fonctions d'aggrégation")
col_agg_num1, col_agg_num2 = st.sidebar.columns(2)

# Choisir une fonction d'aggrégation pour les colonnes numériques
num_agg = col_agg_num1.selectbox(
   "Colonnes numérique",
   num_functions.keys(),
   index = None,
   placeholder = "Calculer",
   disabled = not(group_by)
)

# Choisir une fonction d'aggrégation pour les autres colonnes 
str_agg = col_agg_num2.selectbox(
   "Colonnes textuelle",
   str_functions.keys(),
   index = 0,
   disabled = not(group_by)
)

### TITRE - Affichage

st.sidebar.markdown("# Affichage ")

# Choisir des colonnes à afficher
display = st.sidebar.multiselect(
   "Afficher uniquement",
   columns,
   placeholder = "Afficher"
)

#### LOGIQUE


## Trier

if(order_by):
   df = df.sort_values(order_by, ascending=order)

## Filtrer 

# Custom
if(custom_filter):
   for column in custom_filter:
      column = str(column)
      dtype = df[column].dtype

      # Tester le type
      if dtype == "int64" or dtype == "float64" :   # Numérique
         min = df[column].min()
         max = df[column].max()

         # Créer un slider de filtre
         res = filter_container.slider(column, min, max, (min, max))
         
         # Filtrer
         if(res):
            df = df[df[column].between(res[0], res[1])]

      else:                                        # Autre
         values = df[column].unique()

         # Créer une boîte de selection de filtre
         res = filter_container.multiselect(column, options=values)

         # Filtrer
         if(res):
            df = df[df[column].isin(res)]


# Date de vente
if(date_last and date_first):
   df = df[df["saledate"].between(date_first, date_last)]

# Marque
if(make):
   df = df[df["make"] == make]

# Modele
if(model):
   df = df[df["model"] == model]

# Prix de vente
if(prices[0] and prices[1]):
   df = df[df["sellingprice"].between(prices[0], prices[1])]

## Grouper

if (group_by and num_agg):
   aggregations = {}

   for column in columns:   
      if df[column].dtype == "object":
         aggregations[column] = str_functions[str_agg]
      else:
         aggregations[column] = num_functions[num_agg]
      
   grouped_by = df.groupby(group_by)
   df = grouped_by.agg(func=aggregations)

## Affichage 

if display:
   df = df[(display)]
   


#### VISUALISATION

st.title("Ventes de voitures aux États-Unis")
st.dataframe(df, use_container_width=True)

# L'export en xlsx fait crasher mon PC
# Le dataframe exporté est donc un csv

st.download_button(
   label = "Exporter", 
   data = df.to_csv().encode("utf-8"),       
   file_name = "dataframe.csv",
   mime = "text/csv"
)