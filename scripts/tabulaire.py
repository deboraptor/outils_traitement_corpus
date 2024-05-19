"""
Script pour faire la mise en fichier tabulaire pour la suite.

Ce script permet de scraper des posts et réponses sur Threads, de les nettoyer et de 
les organiser dans un fichier CSV tabulaire. Les étapes principales incluent le scraping 
des données, le nettoyage des données, le traitement des textes, la classification des 
émotions et la sauvegarde des données nettoyées dans un fichier CSV.
"""

import pandas as pd
import nltk

from transformers import pipeline
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from nettoyage import nettoyer_donnees, scrape_thread

# nltk.download("stopwords")
# nltk.download("punkt")
# nltk.download("wordnet")


analyzer = pipeline(
    task="text-classification",
    model="botdevringring/fr-naxai-ai-emotion-classification-081808122023",
    tokenizer="botdevringring/fr-naxai-ai-emotion-classification-081808122023",
)

label_mapping = {
    "sadness": 0,
    "joy": 1,
    "love": 2,
    "anger": 3,
    "fear": 4,
    "surprise": 5,
}


def traiter_texte(texte):
    """
    Effectue la lemmatization et enlève les stop words du texte.

    Args
    ----
        texte (str) : Le texte à traiter.

    Returns
    -------
        str : Le texte traité sans stop words.
    """
    mots = word_tokenize(texte)
    lemmatizer = WordNetLemmatizer()
    mots_lemmatises = [lemmatizer.lemmatize(mot) for mot in mots]
    stop_words = set(stopwords.words("french"))
    mots_filtres = [mot for mot in mots_lemmatises if mot.lower() not in stop_words]
    texte_traite = " ".join(mots_filtres)
    return texte_traite


def fichier_tabulaire(commentaires):
    """
    Crée un DataFrame tabulaire à partir des commentaires avec leurs labels d'émotion.

    Args
    ----
        commentaires (list) : Liste de commentaires à traiter.

    Returns
    -------
        pd.DataFrame : DataFrame contenant les commentaires et leurs labels d'émotion.
    """
    df = pd.DataFrame({"text": commentaires, "label": [""] * len(commentaires)})

    df.insert(0, "", range(len(commentaires)))
    df["label"] = df["text"].apply(
        lambda row: label_mapping[analyzer(traiter_texte(row))[0]["label"]]
    )
    return df


def ecrire_fichier_csv(commentaires, output_file):
    """
    Écrit les commentaires et leurs labels dans un fichier CSV.

    Args
    ----
        commentaires (list) : Liste de commentaires à écrire dans le fichier.
        output_file (str) : Chemin du fichier CSV de sortie.
    """
    df = fichier_tabulaire(commentaires)
    print("Écriture des données dans le fichier CSV")
    with open(output_file, "a", newline="", encoding="utf-8") as f:
        df.to_csv(f, header=f.tell() == 0, index=False)


if __name__ == "__main__":
    print("Début du scraping des threads")
    thread_donnee = scrape_thread("https://www.threads.net/", 50)
    print("Scraping terminé, début du nettoyage des données")
    thread_donnee = nettoyer_donnees(thread_donnee)

    reponses_nettoyees = thread_donnee["reply"]
    commentaires = []

    for reponse in reponses_nettoyees:
        if len(reponse.split()) > 5:
            commentaires.append(reponse)

    print("Réponses de plus de 5 mots : ", commentaires)
    print("Taille du corpus : ", len(commentaires), " commentaires.")

    output_file = "../data/commentaires.csv"
    ecrire_fichier_csv(commentaires, output_file)
    print("Écriture dans le fichier CSV terminée")