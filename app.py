import streamlit as st
import pandas as pd


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

# Dictionnaire des fonctions d'aggrégation, indentifiées par leurs noms

functions = {
   "min":(lambda x: x.min()),
   "max":(lambda x: x.max()),
   "mean":(lambda x: x.mean()),
   "median":(lambda x: x.median())
}

numericals = ["year", "condition", "odometer", "mmr", "sellingprice"]


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
container = st.sidebar.container()

# Choisir une colonne de filtre
custom_filter = container.multiselect(
   "Ajouter un filtre",
   columns,
   placeholder="Choisir une colonne"
)

## Dates des voitures

# Layout des inputs (côte à côte)
col1, col2 = st.sidebar.columns(2)

# Choisir la date de début
date_first = col1.date_input(
   "Vente après le : ",
   value = first_date,
   min_value = first_date, 
   max_value = last_date  
)

# Choisir la date de fin
date_last = col2.date_input(
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

# Choisir les colonnes à afficher
display = st.sidebar.multiselect(
   "Colonnes à afficher", 
   numericals, 
   placeholder="Choisir une colonne",
)

# Choisir une colonne de groupes
group = st.sidebar.selectbox(
   "Regrouper par", 
   columns, 
   index=None, 
   placeholder="Choisir une colonne",
   disabled=not(display)
)


# Choisir une fonction d'aggrégation
aggregation = st.sidebar.selectbox(
   "Fonction d'aggrégation", 
   functions.keys(),
   index=None,
   placeholder="Méthode d'aggrégation",
   disabled=not(group)
)


#### LOGIQUE


## Trier

if(order_by):
   df = df.sort_values(order_by, ascending=order)

## Filtrer 

# Custom
if(custom_filter):
   for col in custom_filter:
      col = str(col)
      dtype = df[col].dtype

      # Tester le type
      if dtype == "int64" or dtype == "float64" :   # Numérique
         min = df[col].min()
         max = df[col].max()

         # Créer un slider de filtre
         res = container.slider(col, min, max, (min, max))
         
         # Filtrer
         if(res):
            df = df[df[col].between(res[0], res[1])]

      else:                                        # Autre
         values = df[col].unique()

         # Créer une boîte de selection de filtre
         res = container.multiselect(col, options=values)

         # Filtrer
         if(res):
            df = df[df[col].isin(res)]


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

if(group and display and aggregation):
   df = functions[aggregation](df.groupby(group)[display])



#### VISUALISATION

st.title("Ventes de voitures aux États-Unis")
st.dataframe(df, use_container_width=True)

st.download_button(
   label = "Exporter", 
   data = df.to_csv().encode("utf-8"),       # L'export en xlsx fait crasher mon PC
   file_name = "dataframe.csv",
   mime = "text/csv"
)