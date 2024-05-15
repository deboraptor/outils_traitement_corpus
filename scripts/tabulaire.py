"""
Script pour faire la mise en fichier tabulaire pour la suite.
"""

from nettoyage import nettoyer_donnees, scrape_thread



if __name__ == "__main__":
    thread_donnee = scrape_thread("https://www.threads.net/?hl=fr", 5)
    thread_donnee = nettoyer_donnees(thread_donnee)

    reponses_nettoyees = thread_donnee["reply"]
    commentaires = []

    for reponse in reponses_nettoyees:
        if len(reponse.split()) > 5:
            commentaires.append(reponse)

    print("Réponses de plus de 5 mots : ", commentaires)
    print("Taille du corpus : ", len(commentaires), " commentaires.")
