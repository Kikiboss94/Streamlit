# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import re

st.markdown(
    """
    <style>
    .stApp { background-color: #000000; }
    h1, h2, h3 { margin: 0; padding: 0; }
    [data-testid="stContainer"] [data-testid="stVerticalBlock"] { margin: 0 !important; padding: 0 !important; }
    .folium-container { padding: 0 !important; margin: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Espaces de coworking à Paris")

df = pd.read_csv('coworking_spaces_idf_cleaned.csv', sep=';', encoding='utf-8')

search = st.text_input("Rechercher un espace", "")
if search:
    df_filtered = df[df['Nom'].str.contains(search, case=False, na=False)]
else:
    df_filtered = df.copy()

if 'arrondissement' not in df_filtered.columns:
    df_filtered['arrondissement'] = df_filtered['Adresse'].apply(
        lambda addr: (
            '1er' if (m:=re.search(r'75 *?(\d{3})', addr)) and int(m.group(1))==1 
            else f"{int(m.group(1))}e"
        ) if isinstance(addr, str) and (m:=re.search(r'75 *?(\d{3})', addr)) and 1<=int(m.group(1))<=20 else None
    )

df_paris = df_filtered[df_filtered['arrondissement'].notnull()]
df_paris = df_paris.dropna(subset=['Latitude', 'Longitude'])

if not df_paris.empty:
    centre_lat = df_paris['Latitude'].astype(float).mean()
    centre_lon = df_paris['Longitude'].astype(float).mean()
else:
    centre_lat, centre_lon = 48.8566, 2.3522

m = folium.Map(location=[centre_lat, centre_lon], zoom_start=12, tiles='CartoDB Positron')
cluster = MarkerCluster().add_to(m)
for _, row in df_paris.iterrows():
    image_html = (
        f"<img src='{row['Image']}' width='200'><br>"
        if 'Image' in row and pd.notna(row['Image']) else ""
    )
    popup_html = (
        f"{image_html}<b>{row['Nom']}</b><br>{row['Adresse']}<br>{row['Téléphone']}<br>"
        f"<a href='{row['Site Web']}' target='_blank'>{row['Site Web']}</a>"
    )
    folium.CircleMarker(
        location=(row['Latitude'], row['Longitude']),
        radius=6,
        color='#000000',
        fill=True,
        fill_color='#000000',
        fill_opacity=0.8,
        popup=folium.Popup(popup_html, max_width=300)
    ).add_to(cluster)

with st.container():
    st.subheader("Carte des espaces de coworking à Paris")
    st_folium(m, width=700, height=500)
    counts = df_paris['arrondissement'].value_counts().reset_index()
    counts.columns = ['arrondissement', 'nombre']
    counts['num'] = counts['arrondissement'].apply(lambda a: 1 if a=='1er' else int(a[:-1]))
    counts = counts.sort_values('num')
    fig, ax = plt.subplots(figsize=(8,4))
    fig.patch.set_facecolor('#000000')
    ax.set_facecolor('#000000')
    ax.bar(counts['arrondissement'], counts['nombre'], color='#F5F5DC')
    ax.set_title("Nombre d'espaces de coworking par arrondissement", color='#F5F5DC')
    ax.set_xlabel("Arrondissement", color='#F5F5DC')
    ax.set_ylabel("Nombre", color='#F5F5DC')
    ax.tick_params(colors='#F5F5DC')
    for spine in ax.spines.values():
        spine.set_color('#F5F5DC')
    st.subheader("Espaces de coworking par arrondissement")
    st.pyplot(fig)
