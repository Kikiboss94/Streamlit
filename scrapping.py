# -*- coding: utf-8 -*-
"""
Scrapping.py
Script de scraping des espaces de coworking en Île-de-France depuis le site leportagesalarial.com,
registre les résultats dans un CSV local.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_coworking_links():
    """
    Récupère les liens des pages de coworking en Île-de-France.
    Renvoie une liste d'URLs.
    """
    base_url = "https://www.leportagesalarial.com/coworking/"
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Erreur lors de la récupération de la page : {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    ile_de_france_prefixes = ['75', '91', '92', '93', '94', '95', '77', '78']
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith("https://www.leportagesalarial.com/coworking/") \
           and any(prefix in href for prefix in ile_de_france_prefixes):
            links.append(href)
    print(f"{len(links)} liens récupérés.")
    return links


def extract_coworking_info(link):
    """
    Extrait les informations de contact d'une page de coworking.
    Renvoie un dict avec Nom, Adresse, Code Postal, Ville, Téléphone, Site Web.
    """
    response = requests.get(link)
    if response.status_code != 200:
        print(f"Erreur lors de la récupération de {link} : {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    info = {
        'Nom': None,
        'Adresse': None,
        'Code Postal': None,
        'Ville': None,
        'Téléphone': None,
        'Site Web': None
    }

    
    title = soup.find('title')
    if title:
        info['Nom'] = title.get_text(strip=True).split(':')[0]

    
    for li in soup.find_all('li'):
        strong = li.find('strong')
        if not strong:
            continue
        key = strong.get_text(strip=True).rstrip(':')
        full_text = li.get_text(separator=' ', strip=True)
        val = full_text.replace(strong.get_text(strip=True), '').strip()

        if key.startswith('Adresse'):
            info['Adresse'] = val
        elif key.startswith('Code Postal'):
            info['Code Postal'] = val
        elif key.startswith('Ville'):
            info['Ville'] = val
        elif key.startswith('Téléphone'):
            info['Téléphone'] = val
        elif key.startswith('Site'):
            
            link_tag = strong.find_next('a')
            info['Site Web'] = link_tag['href'] if link_tag and link_tag.has_attr('href') else val

    return info


def main():
    links = get_coworking_links()
    results = []
    for link in links:
        data = extract_coworking_info(link)
        if data:
            results.append(data)

    
    df = pd.DataFrame(results)
    df.to_csv('coworking_spaces_idf.csv', index=False, sep=';', encoding='utf-8')
    print("Fichier 'coworking_spaces_idf.csv' généré avec succès.")


if __name__ == '__main__':
    main()
