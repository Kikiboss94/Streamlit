README – Visualisation des Espaces de Coworking à Paris

1. Vue d’ensemble

Ce projet collecte, nettoie et visualise les espaces de coworking situés à Paris :

1. Scrapping : récupération automatique des données (nom, adresse, téléphone, site) depuis leportagesalarial.com.
2. Nettoyage / Géocodage : suppression des doublons + ajout des coordonnées GPS grâce à l’API Nominatim (OpenStreetMap).
3. Application Streamlit : carte Folium interactive + graphiques présentant la répartition par arrondissement.

---

2. Arborescence des fichiers

```
mon_projet_coworking/
│
├─ Scrapping.py                  # script de scraping
├─ nettoyage.py                  # nettoyage + géocodage
├─ coworking_spaces_idf.csv      # CSV brut (généré par Scrapping.py)
├─ coworking_spaces_cleaned.csv  # CSV nettoyé (généré par nettoyage.py)
├─ app.py                        # application Streamlit
└─ README.txt                    # ce fichier
```

---

3. Prérequis

Python ≥ 3.9
Modules : `pandas`, `requests`, `beautifulsoup4`, `folium`, `streamlit`, `streamlit_folium`, `matplotlib`, `re` (standard), `time` (standard).
Accès Internet (pour le scraping et le géocodage Nominatim).


4. Étapes d’exécution

 4.1 Scraping des données (`Scrapping.py`)

```bash
python Scrapping.py
```

Fonctions clés

   `get_coworking_links()` : scanne la page principale, sélectionne les URL contenant les préfixes postaux d’Île‑de‑France (75, 91… 78).

   `extract_coworking_info(url)` : parse chaque page avec *BeautifulSoup* et extrait Nom / Adresse / Téléphone / Site Web.

Sortie : `coworking_spaces_idf.csv` (séparateur `;`, encodage UTF‑8, aucune latitude/longitude).

 4.2 Nettoyage et géocodage (`nettoyage.py`)

```bash
python nettoyage.py
```

Fonctions clés

   `geocode_adresse(addr)` : requête HTTP sur Nominatim (format JSON), renvoie `(lat, lon)` ou `(None, None)`.
   `nettoyer_coworking()` :

    1. Lecture robuste du CSV (gestion BOM + `;`).
    2. Renommage des colonnes, suppression doublons, nettoyage texte.
    3. Géocodage (une requête / seconde pour le *rate‑limit*).
    4. Export `coworking_spaces_cleaned.csv`.

4.3 Lancement de l’application Streamlit (`app.py`)

```bash
streamlit run app.py
```

Étapes internes

  1. Charge `coworking_spaces_cleaned.csv`.
  2. Extrait l’arrondissement à partir du code postal (regex `75\d{3}` → `"11e"`).
  3. Carte Folium : fond CartoDB dark\_matter, marqueurs beiges (`#F5F5DC`).
  4. Graphique Matplotlib** : barres beiges sur fond noir (nombre de coworkings / arrondissement).

---

5. Personnalisation rapide

Couleurs : changez `color` et `fill_color` dans la boucle Folium, ou la couleur des barres Matplotlib.
Autres graphiques** : utilisez `streamlit.pyplot()` ou `plotly` pour histogrammes, pie‑charts, etc.
Autres sources** : adaptez `get_coworking_links()` pour d’autres annuaires ou API.

---

