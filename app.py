# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, MiniMap, MeasureControl, LocateControl
from streamlit_folium import st_folium, folium_static
import matplotlib.pyplot as plt
import re


st.markdown("""
<style>
.stApp { background-color: #000000; }
h1, h2, h3 { margin: 0; padding: 0; }
[data-testid="stContainer"] [data-testid="stVerticalBlock"] { margin: 0 !important; padding: 0 !important; }
.folium-container { padding: 0 !important; margin: 0 !important; }
</style>
""", unsafe_allow_html=True)


st.title("Espaces de coworking en Île-de-France")


df = pd.read_csv('coworking_spaces_idf_cleaned.csv', sep=';', encoding='utf-8')


sidebar = st.sidebar
sidebar.title("Filtres")

departments = ['75', '77', '78', '91', '92', '93', '94', '95']
selected_depts = sidebar.multiselect("Départements", departments, default=departments)


df['département'] = df['Adresse'].str.extract(r"\b(\d{2})\d{3}")[0]


if selected_depts:
    df = df[df['département'].isin(selected_depts)]


total = len(df)
st.metric("Total espaces", total)

search = st.text_input("Rechercher un espace", "")
if search:
    df = df[df['Nom'].str.contains(search, case=False, na=False)]

df = df.dropna(subset=['Latitude', 'Longitude'])

if not df.empty:
    centre_lat = df['Latitude'].astype(float).mean()
    centre_lon = df['Longitude'].astype(float).mean()
else:
    centre_lat, centre_lon = 48.8566, 2.3522

m = folium.Map(location=[centre_lat, centre_lon], zoom_start=10, tiles='CartoDB Positron')
cluster = MarkerCluster().add_to(m)
MiniMap().add_to(m)
m.add_child(MeasureControl())
m.add_child(LocateControl())

for _, row in df.iterrows():
    folium.CircleMarker(
        location=(row['Latitude'], row['Longitude']),
        radius=6,
        color='#000000',
        fill=True,
        fill_color='#000000',
        fill_opacity=0.8,
        popup=folium.Popup(
            f"<b>{row['Nom']}</b><br>{row['Adresse']}<br>{row.get('Téléphone','')}<br>"
            f"<a href='{row.get('Site Web','#')}' target='_blank'>{row.get('Site Web','')}</a>",
            max_width=300
        )
    ).add_to(cluster)
folium.LayerControl().add_to(m)


with st.container():
    st.subheader("Carte des espaces de coworking en Île-de-France")
    folium_static(m, width=800, height=500)

    df_plot = df.dropna(subset=['département'])
    counts = df_plot['département'].value_counts().reset_index()
    counts.columns = ['département', 'nombre']
    counts = counts.sort_values('département')

    fig, ax = plt.subplots(figsize=(8,4))
    fig.patch.set_facecolor('#000000')
    ax.set_facecolor('#000000')
    bars = ax.bar(counts['département'], counts['nombre'], color='#F5F5DC')
    
    ax.bar_label(bars, labels=counts['nombre'].tolist(), label_type='edge', color='#F5F5DC')
   
    ax.tick_params(axis='x', colors='#F5F5DC')
    ax.tick_params(axis='y', colors='#F5F5DC')
    ax.set_xlabel("Département", color='#F5F5DC')
    ax.set_ylabel("Nombre d'espaces", color='#F5F5DC')
    plt.tight_layout()

    st.subheader("Espaces de coworking par département")
    st.pyplot(fig)


st.download_button(
    label="Télécharger les données filtrées",
    data=df.to_csv(sep=';', index=False).encode('utf-8'),
    file_name='coworking_filtered.csv',
    mime='text/csv'
)