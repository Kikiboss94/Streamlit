# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import requests
import time


BASE_DIR = os.path.dirname(__file__)
if len(sys.argv) > 1:
    INPUT_CSV = sys.argv[1]
else:
    INPUT_CSV = os.path.join(BASE_DIR, 'coworking_spaces_idf.csv')
base_name = os.path.splitext(os.path.basename(INPUT_CSV))[0]
OUTPUT_CSV = os.path.join(BASE_DIR, f"{base_name}_cleaned.csv")

def geocode_adresse(adresse, timeout=30):
    
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': adresse, 'format': 'json', 'limit': 1}
    headers = {'User-Agent': 'script_geocoding_coworking/1.0'}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"⚠️ Géocodage échoué pour '{adresse}': {e}")
    return None, None


def nettoyer_coworking():
    print(f"🔄 Chargement de '{INPUT_CSV}'...")
    
    df = pd.read_csv(INPUT_CSV, sep=';', encoding='utf-8-sig', dtype=str)

    
    expected_cols = ['Nom','Adresse','Code Postal','Ville','Téléphone','Site Web']
    df.columns = expected_cols[:len(df.columns)]

   
    df = df.drop_duplicates(subset=['Nom','Adresse'])
    df['Adresse']   = df['Adresse'].str.replace(r'^[ :]+','',regex=True).str.strip()
    df['Téléphone'] = df['Téléphone'].str.replace(r'^[ :]+','',regex=True).str.strip()

    
    df = df[df['Nom'].notna() & df['Nom'].str.strip().ne('')]
    df = df[df['Adresse'].notna() & df['Adresse'].str.strip().ne('')]
    df = df.reset_index(drop=True)

    
    if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
        total = len(df)
        print(f"🗺️  Géocodage de {total} adresses (1s pause)...")
        lats, lons = [], []
        for i, adresse in enumerate(df['Adresse'], start=1):
            print(f" [{i}/{total}] {adresse}")
            try:
                lat, lon = geocode_adresse(adresse)
            except Exception as e:
                print(f"⚠️ Erreur inattendue pour '{adresse}': {e}")
                lat, lon = None, None
            lats.append(lat)
            lons.append(lon)
            time.sleep(1)
        df['Latitude'] = lats
        df['Longitude'] = lons
    else:
        print("✅ Colonnes 'Latitude' et 'Longitude' déjà présentes, géocodage ignoré.")

    
    print(f"💾 Export vers '{OUTPUT_CSV}'...")
    df.to_csv(OUTPUT_CSV, sep=';', encoding='utf-8', index=False)
    print("✅ Nettoyage et géocodage terminé.")

if __name__ == '__main__':
    nettoyer_coworking()
