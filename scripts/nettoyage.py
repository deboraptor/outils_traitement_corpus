"""
Ce script va prendre les données récoltées dans le script web_scraping.py et va les 
nettoyer pour préparer leur utilisation avec un modèle d"analyse de sentiments.
"""

import re
from langdetect import detect # va permettre de filtrer les langues pour ne garder que l'anglais

from web_scraping import scrape_thread


def nettoyer_donnees(thread_donnee):
    """
    Nettoie les données.
    
    Args : 
        thread_donnee :

    Returns :
        thread_donnee : renvoie les mêmes données mais nettoyées.
    """
    reponse_unique = []
    for reponse in thread_donnee["reply"]:
        if isinstance(reponse, dict):
            reponse_texte = reponse.get("text", "")
        elif isinstance(reponse, str):
            reponse_texte = reponse
        else:
            # print("Type d'élément non géré dans la liste "reply":", type(reponse))
            continue

        reponse_texte = supprimer_urls(reponse_texte)  
        reponse_texte = supprimer_emojis(reponse_texte)  
        reponse_texte = supprimer_retours_chariots(reponse_texte)
        reponse_texte = supprimer_username(reponse_texte) 
        reponse_texte = supprimer_hashtags(reponse_texte)
        reponse_texte = supprimer_ponctuation(reponse_texte)
        reponse_texte = supprimer_chaine_vide(reponse_texte)
        reponse_texte = supprimer_espaces(reponse_texte)
        reponse_texte = supprimer_caractere_speciaux(reponse_texte)

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
    regex_url = r"https?://\S+|www\.\S+"
    texte_sans_urls = re.sub(regex_url, "", texte)
    return texte_sans_urls


def supprimer_emojis(texte):
    """
    Supprime les émojis d'une chaîne de caractères.
    """
    texte_sans_emojis = re.sub(r"[^\x00-\x7F]+", "", texte)
    return texte_sans_emojis


def supprimer_retours_chariots(texte):
    """
    Supprime les retours chariots d'une chaîne de caractères.
    """    
    texte_sans_retours_chariots = re.sub(r"\n", "", texte)
    return texte_sans_retours_chariots


def supprimer_username(texte):
    """
    Supprime les noms des utilisateurs d'une chaîne de caractères.
    """    
    texte_sans_username = re.sub(r"@[^\s@]+\b", "", texte)
    return texte_sans_username


def supprimer_hashtags(texte):
    """
    Supprime les hastags d'une chaîne de caractères.
    """
    # j'ai décidé de garder le texte après qui peut être utile pour l'analyse
    texte_sans_hashtags = re.sub(r"#", " ", texte)
    return texte_sans_hashtags


def supprimer_chaine_vide(texte):
    """
    Supprime les chaînes vides d'une chaîne de caractères.
    """    
    texte_sans_chaine_vide = re.sub(r"^\s*$", "", texte)
    return texte_sans_chaine_vide


def supprimer_ponctuation(texte):
    """
    Supprime la ponctuation d'une chaîne de caractères.
    """
    texte_sans_ponctuation = re.sub(r"[^\w\s_\D|]", "", texte)
    return texte_sans_ponctuation


def supprimer_espaces(texte):
    """
    Supprime les espaces d'une chaîne de caractères.
    """
    texte_sans_espaces = re.sub(r"\s+", " ", texte)
    return texte_sans_espaces


def supprimer_caractere_speciaux(texte):
    """
    Supprime les caractères spéciaux d'une chaîne de caractères.
    """
    texte_sans_caractere_speciaux = re.sub(r"[^\w\s]", "", texte)
    return texte_sans_caractere_speciaux