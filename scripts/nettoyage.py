"""
Ce script va prendre les données récoltées dans le script web_scraping.py et va les 
nettoyer pour préparer leur utilisation avec un modèle d'analyse de sentiments.

Il exécute la fonction scrape_thread() dans le main du script tabulaire.py.
"""

import re

from web_scraping import scrape_thread


def nettoyer_donnees(thread_donnee):
    """
    Nettoie les données en appliquant plusieurs étapes de prétraitement.
    
    Args 
    ----
        thread_donnee (dict) : dictionnaire contenant les données de threads et de réponses.

    Returns
    -------
        dict : dictionnaire qui contient les mêmes données mais nettoyées.
    """
    reponses_uniques = []
    for reponse in thread_donnee["reply"]:
        if isinstance(reponse, dict):
            reponse_texte = reponse.get("text", "")
        elif isinstance(reponse, str):
            reponse_texte = reponse
        else:
            continue

        reponse_texte = appliquer_nettoyage(reponse_texte)
        if reponse_texte and reponse_texte not in reponses_uniques and detect_langue(reponse_texte) == 'en':
            reponses_uniques.append(reponse_texte)

    thread_donnee["reply"] = reponses_uniques
    return thread_donnee


def appliquer_nettoyage(texte):
    """
    Applique une série d'étapes de nettoyage sur le texte.

    Args
    ----
        texte (str) : le texte à nettoyer.

    Returns
    -------
        str : le texte nettoyé.
    """
    # Supprimer les URLs
    texte = re.sub(r"https?://\S+|www\.\S+", "", texte)
    # Supprimer les émojis et les caractères non ASCII
    texte = re.sub(r"[^\x00-\x7F]+", "", texte)
    # Supprimer les retours chariots
    texte = re.sub(r"\n", "", texte)
    # Supprimer les noms d'utilisateurs
    texte = re.sub(r"@[^\s@]+\b", "", texte)
    # Remplacer les hashtags par des espaces
    texte = re.sub(r"#", " ", texte)
    # Supprimer la ponctuation
    texte = re.sub(r"[^\w\s]", "", texte)
    # Supprimer les chaînes vides
    texte = re.sub(r"^\s*$", "", texte)
    # Supprimer les espaces en trop
    texte = re.sub(r"\s+", " ", texte)
    # Supprimer les caractères spéciaux restants
    texte = re.sub(r"[^\w\s]", "", texte)

    # Supprimer les espaces en début et fin de chaîne et mettre en minuscule
    texte = texte.strip().lower()
    return texte