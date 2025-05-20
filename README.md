Streamlit Kilian

🏢 Présentation du projet

Le projet **Streamlit Kilian** est une application web de visualisation de données qui cible les espaces de coworking en Île-de-France. Il récupère automatiquement les informations de chaque espace depuis le site leportagesalarial.com, puis effectue un nettoyage et un géocodage de ces données. Enfin, l’application affiche ces espaces sur une carte interactive Folium intégrée dans une interface Streamlit, permettant d’explorer facilement leur répartition géographique.

✨ Fonctionnalités

* **Scraping automatique :** récupération des données (nom, adresse, téléphone, site web) depuis les pages coworking du site leportagesalarial.com pour l’Île-de-France.
* **Nettoyage et géocodage :** suppression des doublons, nettoyage des textes et géocodage des adresses (obtenir latitude/longitude via l’API Nominatim d’OpenStreetMap).
* **Carte interactive :** visualisation des espaces de coworking sur une carte Folium avec marqueurs (cluster) et popups informatifs (nom, adresse, téléphone, lien web).
* **Recherche par nom :** champ de recherche pour filtrer dynamiquement les espaces selon leur nom.
* **Affichage par département :** détection du département  de chaque adresse et regroupement sur la carte.
* **Graphique de répartition :** diagramme à barres (Matplotlib) affichant le nombre d’espaces de coworking par département d'Ile de France.

🧾 Dépendances principales

Streamlit – Création d'interfaces web interactives.
Pandas – Manipulation et analyse de données.
Requests – Requêtes HTTP.
BeautifulSoup – Analyse de documents HTML.
Folium – Cartographie interactive.
Geopy – Géocodage d'adresses.

🛠️ Installation

Suivez ces étapes pour installer et lancer le projet :

```bash
# Cloner le dépôt GitHub
git clone https://github.com/Kikiboss94/Streamlit
cd Streamlit-Kilian

# Créer et activer un environnement virtuel (Linux/Mac)
python3 -m venv env
source env/bin/activate

# (Windows : utilisez 'env\Scripts\activate')
# Installer les dépendances requises
pip install pandas requests beautifulsoup4 streamlit folium streamlit-folium matplotlib

# Exécuter le script de scraping pour collecter les données
python scrapping.py

# Exécuter le script de nettoyage et géocodage
python nettoyage.py

# Lancer l’application Streamlit
streamlit run app.py
```

📁 Arborescence du projet

```
Streamlit-Kilian/
├── scrapping.py                  # Script de scraping des données
├── nettoyage.py                  # Script de nettoyage et géocodage
├── app.py                        # Application Streamlit principale
├── rquirements.txt               # Liste des dépendences nécessaires
├── coworking_spaces_idf.csv      # Données brutes récupérées (avant nettoyage)
├── coworking_spaces_idf_cleaned.csv  # Données nettoyées et géocodées
└── README.md                     # Ce fichier README
```

📄 Explications des scripts

* scrapping.py – Ce script recueille automatiquement les informations des espaces de coworking.

  * get\_coworking\_links() : explore la page principale du site pour extraire les URLs des pages coworking correspondant aux départements d’Île-de-France.
  * extract\_coworking\_info(link) : visite chaque URL récupérée et extrait les détails (nom, adresse, code postal, ville, téléphone, site web) en analysant le contenu HTML.
  * *main()* : combine les fonctions ci-dessus pour générer un fichier CSV (`coworking_spaces_idf.csv`) contenant toutes les données collectées.

* nettoyage.py – Ce script nettoie les données brutes et réalise le géocodage des adresses.

  * geocode\_adresse(adresse) : envoie une requête à l’API Nominatim (OpenStreetMap) pour obtenir les coordonnées GPS (latitude, longitude) d’une adresse.
  * nettoyer\_coworking() : charge le CSV initial, renomme les colonnes, supprime les doublons, nettoie les champs texte (trim, suppressions des préfixes “: ”) et filtre les enregistrements valides. Si les colonnes Latitude et Longitude n’existent pas, le script géocode chaque adresse (avec une pause d’1s entre chaque requête pour respecter l’API) et ajoute ces coordonnées. Les données nettoyées sont enregistrées dans `coworking_spaces_idf_cleaned.csv`.

* app.py – Il s’agit du cœur de l’application Streamlit qui affiche les données.

  * Chargement des données propres (`coworking_spaces_idf_cleaned.csv`) dans un DataFrame Pandas.
  * Champ de recherche (`st.text_input`) pour filtrer les espaces selon le nom saisi.
  * Calcul automatique du **département en Ile de France** à partir de l’adresse (recherche regex sur le code postal « 75xxx »).
  * Création d’une carte **Folium** centrée sur la moyenne des coordonnées, avec un *MarkerCluster* pour regrouper les points. Pour chaque espace, un marqueur (ici un cercle noir) est ajouté avec un popup contenant le nom, l’adresse, le téléphone et un lien vers le site web.
  * Affichage de la carte interactive dans Streamlit via `st_folium`.
  * Génération d’un graphique Matplotlib (barres) montrant le **nombre d’espaces par département**. Ce graphique est stylisé pour s’harmoniser avec l’interface et affiché avec `st.pyplot`.

📊 Aperçu des visualisations

L’application propose deux visualisations principales :

* Carte interactive Folium : affiche tous les espaces de coworking filtrés sur une carte de l'Ile de France. Les marqueurs sont groupés en clusters lors du zoom-out. Cliquer sur un marqueur ouvre une fenêtre popup avec les informations détaillées (nom, adresse, téléphone, site web). Le champ de recherche permet de ne visualiser que les espaces correspondant au terme saisi.
* Graphique par département : sous la carte, un diagramme à barres représente le nombre d’espaces de coworking pour chaque département d'Ile de France. Cela permet de voir rapidement la répartition géographique en un coup d’œil.

📌 À propos

Streamlit Kilian est un projet d’apprentissage visant à développer une application web de visualisation de données. Il permet de mettre en pratique le scraping de données, le nettoyage/traitement en Python, et la création d’une interface interactive avec Streamlit et Folium. Le ton pédagogique du README reflète l’objectif de partager les étapes clés du développement.

📄 Licence

Aucune licence spécifique n’a été définie pour ce projet. Il est fourni tel quel pour un usage éducatif et libre. Les contributeurs peuvent l’adapter ou l’améliorer selon leurs besoins.
