"""
Ce script permet d'automatiser l'extraction de posts et de réponses sur le site 
Threads, de les filtrer et de les organiser.

Il éxecute la fonction scrape_thread() dans le main du script tabulaire.py.
"""

import json
import jmespath # permet de faire des requêtes JSON

from typing import Dict 
from tqdm import tqdm # ajoute une bar de progression pour connaître le temps de chargement
from parsel import Selector # pour extraire des données HTML
from nested_lookup import nested_lookup # permet de rechercher des clés spécifiques dans des strucures de données imbriquées
from playwright.sync_api import sync_playwright # sert pour naviguer automatiquement dans des pages web


def parse_thread(donnee: Dict) -> Dict:
    """
    Cette fonction prend un dictionnaire JSON (donnee) représentant un post de Thread 
    et utilise jmespath pour extraire le texte du post. Elle retourne un dictionnaire 
    contenant le texte du post.

    Args :
        donnee (Dict) : dictionnaire de données JSON contenant les informations sur 
        le post Thread.

    Returns :
        Dict : dictionnaire contenant le texte du post Thread.
    """

    resultat = jmespath.search(
        """{
        text: post.caption.text
    }""",
        donnee,
    )
    return resultat

def scrape_thread(url: str, max_pages: int) -> dict:
    """
    Scrape les posts et les réponses sur Threads à partir d'une URL donnée, sur un 
    nombre spécifié de pages.
    
    Args :
        url (str) : URL de la page Threads à scraper.
        max_pages (int) : correspond au nombre maximum de pages à scraper.
    
    Returns : 
        dict : dictionnaire contenant le texte du premier post sous la clé "thread"
        et une liste des textes des réponses sous la clé "reply". Si aucun post n'est 
        trouvé, retourne un dictionnaire avec des valeurs vides.
    
    """
    threads = []
    for page_num in range(1, max_pages + 1):
        with sync_playwright() as pw:
            navigateur = pw.chromium.launch()
            contexte = navigateur.new_context(viewport={"width": 1920, "height": 1080})
            page = contexte.new_page()
            page.set_default_timeout(60000)

            with tqdm(total=max_pages, desc="Scraping en cours ☻", colour="magenta") as pbar:
                for page_num in range(1, max_pages + 1):
                    try:
                        page.goto(f"{url}?page={page_num}")
                        page.wait_for_load_state("networkidle")
                        page.wait_for_selector("[data-pressable-container=true]")
                        selector = Selector(page.content())
                        datasets_caches = selector.css('script[type="application/json"][data-sjs]::text').getall()

                        for dataset_cache in datasets_caches:
                            if '"ScheduledServerJS"' not in dataset_cache:
                                continue
                            if "thread_items" not in dataset_cache:
                                continue
                            donnee = json.loads(dataset_cache)

                            thread_items = nested_lookup("thread_items", donnee)
                            if not thread_items:
                                continue
                            parsed_threads = [parse_thread(t) for thread in thread_items for t in thread]
                            threads.extend(parsed_threads)

                        pbar.update(1)  

                    except Exception as e:
                        print(f"Erreur: {e}")
            navigateur.close()

    if threads:
        return {
            "thread": threads[0]["text"],
            "reply": [reponse["text"] for reponse in threads[1:]],
        }
    else:
        return {
            "thread": "",
            "reply": []
        }