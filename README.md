# Sommaire
* [Outils Traitement Corpus](#outils-traitement-corpus)
	+ [Le projet que je veux réaliser](#le-projet-que-je-veux-réaliser)
	+ [Le dataset que j'ai choisi](#le-dataset-que-jai-choisi)
		- [Comment ont été collectées les données ?](#comment-ont-été-collectées-les-données-)
		- [À quoi peut servir ce corpus ?](#à-quoi-peut-servir-ce-corpus-)
		- [À quel modèle a-t-il servi ?](#à-quel-modèle-a-t-il-servi-)
		- [Exemple](#exemple)
	+ [À moi de jouer !](#à-moi-de-jouer-)
		- [Idées](#idées)
		- [Objectifs pour la prochaine fois](#objectifs-pour-la-prochaine-fois)
	+ [Nettoyage des données](#nettoyage-des-données)
		- [Tâches de nettoyage](#tâches-de-nettoyage)

# Outils Traitement Corpus
## Le projet que je veux réaliser
J'aimerais bien me lancer dans un projet d'analyse de sentiments car ça m'intéresse beaucoup et j'ai envie de comprendre mieux comment ça fonctionne. 

![image](https://github.com/deboraptor/outils_traitement_corpus/assets/145542205/bc3a2483-1f69-4aad-8514-7444fda1e554)


#### brouillon
J'ai décidé de mettre sur le git le fichier de la dataset de _Kaggle_ parce que ce dépôt git est plus qu'un projet en cours, c'est aussi un dépôt sur lequel je veux revenir souvent et améliorer au fur et à mesure en apprenant de nouvelles choses plus tard. 

J'ai donc des fichiers qui sont pour mon enrichissement personnel, des fichiers tests qui ne sont pas utiles pour le cours et j'ai décidé de les garder sur le git mais de les mettre dans mon .gitignore temporairement pour la correction.

### Le dataset que j'ai choisi
J'ai trouvé un dataset sur _Kaggle_ qui correspond totalement à mon projet ! Le dataset se nomme <a href="https://www.kaggle.com/datasets/nelgiriyewithana/emotions">Emotions</a> et permet d'analyser de courts messages postés en ligne selon 6 types d'émotions :
* tristesse (0)
* joie (1)
* amour (2)
* colère (3)
* peur (4) 
* surprise (5)

Ces émotions sont classées de 0 à 5 selon l'émotion primaire qui ressort du message.

### Comment ont été collectées les données ?
Les données ici ont été récoltées sur _Twitter_, le réseau social très populaire. Il y a 416 808 phrases au total et elles ont toutes la même forme : "I [VERB] [..]". Voici un exemple du début du document que j'ai pu télécharger sur _Kaggle_.

![image](https://github.com/deboraptor/outils_traitement_corpus/assets/145542205/0e56f652-54ef-4524-9269-35a587ca3b01)

### À quoi peut servir ce corpus ?
* Analyse de sentiment
* Classification des émotions
* Analyse textuelle

### À quel modèle a-t-il servi ?
J'ai pu voir que ce dataset a été réutilisée par 39 autres personnes, c'est aussi l'un des plus populaire de ce site. Ces notebooks vont m'être très utiles par la suite. Je crois que c'est un dataset assez récent car il a été modifié pour la dernière fois il y a 2 mois, donc il n'y a pas encore beaucoup de modèles qui ont pu l'utiliser. 

### Exemple
Voici un exemple de comment ça fonctionne.

![image](https://github.com/deboraptor/outils_traitement_corpus/assets/145542205/e04facce-d28b-4522-b2fc-83380b759a57)

On voit bien qu'il y a le message sous forme de chaînes de caractères et la classification de l'émotion sous forme de chiffre de 0 à 5 comme on l'avait vu au-dessus. 

## À moi de jouer ! 
Je vais récolter les données en français ! 

Threads n’a pas d’API publique, donc j’ai décidé d’utiliser `PlayWright` pour parser le site. Comme je ne pouvais pas l'utiliser dans mon Jupyter Notebook, je suis passée sur un fichier python classique. 

Un problème s’est alors posé devant moi : quels commentaires je prends ? Comme je ne peux pas parser tout le site sans le faire planter ou me faire bannir, je dois fixer des limites.

### Idées 
J'aimerais bien le faire avec plusieurs classes de différents acteurs ou chanteurs, comme ça on pourrait voir lesquels sont les plus appréciés ou pas.

Et pourquoi pas regarder chaque commentaire et comparer le sentiment "moyen" de chaque post en fonction du titre et en porter des conclusions grâce à l'analyse de sentiments (?)

Objectifs pour la prochaine fois : 
- [ ] récupérer le dernier commentaire posté
- [ ] augmenter la portée aux derniers 25 commentaires postés max
- [ ] récupérer toutes les réponses de ces commentaires

### Nettoyage des données
Pour pouvoir exploiter les données correctement, il va falloir commencer le nettoyage des données. En lançant le script qui récupère les threads, je vais tout d'abord repérer les choses qu'il va falloir nettoyer ci-dessous :
- [X] tout mettre en minuscule
- [X] supprimer toute forme de ponctuation
    + [ ] et les $ ?
    + [ ] les nombres aussi ?
- [X] enlever les URLs
    + [ ] enlever aussi celles sans le https (instagram.com/p/c6-qrpgsm0h/)
- [ ] vérifier la langue (prendre que le français)
- [X] enlever les hastags (mais garder le texte ? -> oui)
- [X] supprimer les \n 
- [X] corriger les chaînes de caractères vides
    + [ ] corriger les chaînes sans mots (par exemple : "    ...     ")
- [X] enlever les mentions (qui commencent par un @)
- [X] ne prendre que les phrases de 3 mots ou plus (pour que l'analyse soit plus juste)

### Fichier tabulaire
est-ce que je dois faire exactement comme la dataset et mettre toutes les phrases qui 
commencent par "i [...]" ?