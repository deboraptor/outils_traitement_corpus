# Sommaire
* [Outils Traitement Corpus](#outils-traitement-corpus)
  + [Le projet que je veux réaliser](#le-projet-que-je-veux-réaliser)
  + [Le dataset que j'ai choisi](#le-dataset-que-jai-choisi)
    - [Comment ont été collectées les données ?](#comment-ont-été-collectées-les-données)
    - [À quoi peut servir ce corpus ?](#à-quoi-peut-servir-ce-corpus)
    - [À quel modèle a-t-il servi ?](#à-quel-modèle-a-t-il-servi)
    - [Exemple](#exemple)
  + [À moi de jouer !](#à-moi-de-jouer)
    - [Extraction des données](#extraction-des-données)
    - [Nettoyage des données](#nettoyage-des-données)
  + [Mes scripts](#mes-scripts)
    - [Lancement d'un environnement virtuel](#lancement-dun-environnement-virtuel)
    - [Installer les modules](#installer-les-modules)
    - [Lancement des scripts](#lancement-des-scripts)

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
Threads n’a pas d’API publique, donc j’ai décidé d’utiliser `PlayWright` pour parser le site. Comme je ne pouvais pas l'utiliser dans mon Jupyter Notebook, je suis passée sur un fichier python classique. 

Un problème s’est alors posé devant moi : quels commentaires je prends ? Comme je ne peux pas parser tout le site sans le faire planter ou me faire bannir, je dois fixer des limites.

### Extraction des données
J'ai voulu prendre des données en français mais je n'ai pas réussi. J'ai tenté de
récolter les commentaires avec l'attribut **lang** dans la balise html `lang="fr"` dans le code source, mais le site ne possède que la balise `lang="en"`, même lorsque c'est en français. 

### Nettoyage des données
Pour pouvoir exploiter les données correctement, il va falloir commencer le nettoyage des données. En lançant le script qui récupère les threads, je vais tout d'abord repérer les choses qu'il va falloir nettoyer ci-dessous :
- [X] tout mettre en minuscule
- [X] supprimer toute forme de ponctuation
    + [X] et les $ ?
    + [ ] les nombres aussi ?
- [X] enlever les URLs
    + [ ] enlever aussi celles sans le https (instagram.com/p/c6-qrpgsm0h/)
- [ ] vérifier la langue (prendre que le français)
- [X] enlever les hastags (mais garder le texte ? -> oui)
- [X] supprimer les \n 
- [X] corriger les chaînes de caractères vides
    + [X] corriger les chaînes sans mots (par exemple : "    ...     ")
- [X] enlever les mentions (qui commencent par un @)
- [X] ne prendre que les phrases de 3 mots ou plus (pour que l'analyse soit plus juste)

## Mes scripts
### Lancement d'un environnement virtuel
Pour éviter les conflits de version, nous allons créer un environnement virtuel. 
Pour créer un environnement virtuel, vous pouvez procéder comme suit : 

```python3 -m venv nom_du_venv``` 

Ensuite, il va vous falloir activer l’environnement. 

```source nom_du_venv/bin/activate```

Lorsque c’est fait, vous verrez entre parenthèse le nom de votre environnement tout à
gauche de la ligne de commande. 

N’oubliez pas de désactiver l’environnement lorsque vous avez terminé. 

```deactivate```

### Installer les modules
Avant de pouvoir lancer les scripts, il faut que vous ayez les bons modules installés dans votre environnement virtuel. Pour cela, il vous suffit simplement de lancer la commande suivante :

```pip install -r requirements.txt```

### Lancement des scripts
Pour lancer le scraping du web, le nettoyage des données et la mise en format tabulaire, il suffit simplement de lancer le fichier tabulaire.py. Vous pouvez le faire de cette manière : 

```python3 tabulaire.py```

Grâce à la fonction main et à l'importation des fichiers, les trois scripts se lancent en même temps.