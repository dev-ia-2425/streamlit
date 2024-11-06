import streamlit as st
import pandas as pd

st.set_page_config( layout="wide" )

source = pd.read_csv("car_prices_clean.csv", encoding='utf-8', delimiter=",")
df = source

columns = df.columns
brands = df["make"].unique()

models = df["model"].unique()

min_price = df["sellingprice"].min()
max_price = df["sellingprice"].max()
mid_price = (max_price - min_price) / 2

df["saledate"] = pd.to_datetime(df["saledate"], format="mixed").dt.date

first_date = df["saledate"].min()
last_date = df["saledate"].max()

# INPUTS

st.sidebar.markdown("# Trier les lignes")    # Tri

# Colonne de tri
order_by = st.sidebar.selectbox(
   "Trier sur cette colonne", 
   columns, 
   index=None, 
   placeholder="Choisir une colonne"
)

# Type de tri
order = ("Croissant" == (st.sidebar.selectbox("Type de tri", ["Croissant", "Décroissant"])))


st.sidebar.markdown("# Filter les lignes")   # Filtres

# Filtre custom 
filter = st.sidebar.multiselect(
   "Ajouter un filtre"
)

# Fourchette de dates

col1, col2 = st.sidebar.columns(2)

date_first = col1.date_input(
   "Après le : ",
   value = first_date,
   min_value = first_date, 
   max_value = last_date  
)

date_last = col2.date_input(
   "Avant le : ",
   value = last_date,
   min_value = date_first, 
   max_value = last_date
)

# Marque
make = st.sidebar.selectbox("Marque du véhicule", brands, index=None, placeholder="Choisir une marque")

# Modèle 
if(make):
   models = df[df["make"] == make]["model"].unique()

model = st.sidebar.selectbox("Modèle du véhicule", models, index=None, placeholder="Choisir un modèle")

# Fourchette de prix
prices = st.sidebar.slider("Prix de vente", min_price, max_price, (min_price, max_price))





st.sidebar.markdown("# Grouper par")   # Groupes


# LOGIQUE

# Tri
if(order_by):
   df = df.sort_values(order_by, ascending=order)

# Filtre - Date de vente
if(date_last and date_first):
   df = df[df["saledate"].between(date_first, date_last)]

# Filtre - Marque
if(make):
   df = df[df["make"] == make]

# Filtre - Modele
if(model):
   df = df[df["model"] == model]

# Filtre - Prix de vente
if(prices[0] and prices[1]):
   df = df[df["sellingprice"].between(prices[0], prices[1])]


# DATAFRAME
st.title("Ventes de voitures aux États-Unis")
st.dataframe(df, use_container_width=True)

st.download_button(
   label = "Exporter", 
   data = df.to_csv().encode("utf-8"),
   file_name = "dataframe.csv",
   mime = "text/csv"
)