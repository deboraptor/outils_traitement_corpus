"""
Ce script va prendre les données récoltées dans le script web_scraping.py et 
va les nettoyer pour préparer leur utilisation avec un modèle d'analyse de sentiments.
"""

import re

from web_scraping import scrape_thread

def nettoyer_donnees(thread_donnee):
    """
    Supprime les doublons et les émojis dans la liste des réponses.
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