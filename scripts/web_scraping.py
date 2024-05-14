import json
import re
import emoji

from typing import Dict

import jmespath
from parsel import Selector
from nested_lookup import nested_lookup
from playwright.sync_api import sync_playwright

def parse_thread(donnee: Dict) -> Dict:
    """
    Extrait le texte du post Thread à partir d'un dictionnaire de données JSON.

    Args:
        donnee (Dict): Dictionnaire de données JSON contenant les informations sur le post Thread.

    Returns:
        Dict: Dictionnaire contenant le texte du post Thread.
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
    Scrape les données d'un thread Threads à partir de son URL et jusqu'à un nombre maximal de pages.

    Args:
        url (str): L'URL du thread Threads à scraper.
        max_pages (int): Le nombre maximal de pages à scraper pour ce thread.

    Returns:
        dict: Un dictionnaire contenant les données du thread, avec les clés "thread" pour le
               message original et "reply" pour les réponses.
    """

    threads = []
    for page_num in range(1, max_pages + 1):
        with sync_playwright() as pw:
            navigateur = pw.chromium.launch()
            contexte = navigateur.new_context(viewport={"width": 1920, "height": 1080})
            page = contexte.new_page()

            page.goto(f"{url}?page={page_num}")
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
    return {
        "thread": threads[0]["text"],
        "reply": [reponse["text"] for reponse in threads[1:]],
    }

def nettoyer_donnees(thread_donnee):
    """
    Nettoie les données du thread en supprimant les doublons et les caractères indésirables dans les réponses.

    Args:
        thread_data (dict): Dictionnaire contenant les données du thread à nettoyer.

    Returns:
        dict: Dictionnaire contenant les données nettoyées du thread.
    """

    reponse_unique = []
    for reponse in thread_donnee["reply"]:
        if isinstance(reponse, dict):
            reponse_texte = reponse.get("text", "")
        elif isinstance(reponse, str):
            reponse_texte = reponse
        else:
            print("Type d'élément non géré dans la liste 'reply':", type(reponse))
            continue

        if reponse_texte not in reponse_unique:
            reponse_unique.append(reponse_texte)

    reponse_unique_nettoyes = []
    for reponse in reponse_unique:
        reponse_nettoye = re.sub(r'[^\x00-\x7F]+', '', reponse)
        reponse_unique_nettoyes.append(reponse_nettoye)

    thread_donnee["reply"] = reponse_unique_nettoyes

    return thread_donnee


if __name__ == "__main__":
    thread_donnee = scrape_thread("https://www.threads.net/t/CuVdfsNtmvh/", 5)
    thread_donnee = nettoyer_donnees(thread_donnee)

    print("Thread :", thread_donnee["thread"])
    print("Réponses :", thread_donnee["reply"])
