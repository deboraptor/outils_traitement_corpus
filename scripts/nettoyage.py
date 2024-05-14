"""
Ce script va prendre les données récoltées dans le script web_scraping.py et 
va les nettoyer pour préparer leur utilisation avec un modèle d'analyse de sentiments.
"""

import re

from web_scraping import scrape_thread


def nettoyer_donnees(thread_donnee):
    """
    Supprime les doublons, les émojis et les URLs dans la liste des réponses.
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

        reponse_texte = supprimer_urls(reponse_texte)  
        reponse_texte = supprimer_emojis(reponse_texte)  
        reponse_texte = supprimer_retours_chariots(reponse_texte)
        reponse_texte = supprimer_username(reponse_texte) 
        reponse_texte = supprimer_hashtags(reponse_texte)
        reponse_texte = supprimer_ponctuation(reponse_texte)
        reponse_texte = supprimer_chaine_vide(reponse_texte)
        reponse_texte = supprimer_espaces(reponse_texte)

        reponse_texte = reponse_texte.strip()
        reponse_texte = reponse_texte.lower()

        if reponse_texte not in reponse_unique:
            reponse_unique.append(reponse_texte)

    thread_donnee["reply"] = reponse_unique
    return thread_donnee


def supprimer_urls(texte):
    """
    Supprime les URLs d'une chaîne de caractères.
    """

    regex_url = r'https?://\S+|www\.\S+'
    texte_sans_urls = re.sub(regex_url, '', texte)
    return texte_sans_urls


def supprimer_emojis(texte):
    """
    Supprime les émojis d'une chaîne de caractères.
    """

    texte_sans_emojis = re.sub(r'[^\x00-\x7F]+', '', texte)
    return texte_sans_emojis


def supprimer_retours_chariots(texte):
    
    texte_sans_retours_chariots = re.sub(r'\n', '', texte)
    return texte_sans_retours_chariots


def supprimer_username(texte):
    
    texte_sans_username = re.sub(r'@[^\s@]+\b', '', texte)
    return texte_sans_username


def supprimer_hashtags(texte):

    # je décide de garder le texte après qui peut être utile pour l'analyse
    texte_sans_hashtags = re.sub(r'#', ' ', texte)
    return texte_sans_hashtags


def supprimer_chaine_vide(texte):
    
    texte_sans_chaine_vide = re.sub(r'^\s*$', '', texte)
    return texte_sans_chaine_vide


def supprimer_ponctuation(texte):
    texte_sans_ponctuation = re.sub(r'[^\w\s_]', '', texte)
    return texte_sans_ponctuation


def supprimer_espaces(texte):
    texte_sans_espaces = re.sub(r'\s+', ' ', texte)
    return texte_sans_espaces


if __name__ == "__main__":
    thread_donnee = scrape_thread("https://www.threads.net/", 25)
    thread_donnee = nettoyer_donnees(thread_donnee)

    print("Thread :", thread_donnee["thread"])
    print("Réponses :", thread_donnee["reply"])