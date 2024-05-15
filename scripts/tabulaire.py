"""
Script pour faire la mise en fichier tabulaire pour la suite.
"""

import csv

import pandas as pd

from nettoyage import nettoyer_donnees, scrape_thread


def fichier_tabulaire(commentaires):
    df = pd.DataFrame({
        "text": commentaires,
        "label": [""] * len(commentaires)
    })

    df.insert(0, "", range(len(commentaires)))
    df.to_csv("commentaires.csv", index=False)


def ecrire_fichier_csv(commentaires):

    with open("../data/clean/commentaires.csv", "w", newline="", encoding="utf-8") as f:
        ecrivain = csv.writer(f)
        ecrivain.writerow(["", "text", "label"])

        for i, commentaire in enumerate(commentaires):
            ecrivain.writerow([i, commentaire, ""])


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
