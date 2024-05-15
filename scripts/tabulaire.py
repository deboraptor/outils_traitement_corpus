"""
Script pour faire la mise en fichier tabulaire pour la suite.
"""

import csv
import random

import pandas as pd

from nettoyage import nettoyer_donnees, scrape_thread


def fichier_tabulaire(commentaires):
    df = pd.DataFrame({
        "text": commentaires,
        "label": [""] * len(commentaires)
    })

    df.insert(0, "", range(len(commentaires)))

    df["label"] = df.apply(lambda row: random.randint(0, 5), axis=1)

    return df


def ecrire_fichier_csv(commentaires):
    df = fichier_tabulaire(commentaires)

    with open("../data/clean/commentaires.csv", "w", newline="", encoding="utf-8") as f:
        ecrivain = csv.writer(f)
        ecrivain.writerow(["", "text", "label"])

        for i, row in df.iterrows():
            ecrivain.writerow([i, row["text"], row["label"]])


if __name__ == "__main__":
    thread_donnee = scrape_thread("https://www.threads.net/?hl=fr", 30)
    thread_donnee = nettoyer_donnees(thread_donnee)

    reponses_nettoyees = thread_donnee["reply"]
    commentaires = []

    for reponse in reponses_nettoyees:
        if len(reponse.split()) > 5:
            commentaires.append(reponse)

    print("Réponses de plus de 5 mots : ", commentaires)
    print("Taille du corpus : ", len(commentaires), " commentaires.")

    fichier_tabulaire(commentaires)
    ecrire_fichier_csv(commentaires)

    # python3 tabulaire.py > ../data/raw/commentaires.txt