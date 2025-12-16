# Projet Python – Exploration d’un corpus sur l’Intelligence Artificielle

## Présentation générale

Il consiste à construire, structurer et exploiter un **corpus de documents textuels** issus de plusieurs sources (Reddit et Arxiv), puis à proposer une **interface interactive** permettant d’explorer ce corpus.

Le projet couvre l’ensemble de la chaîne :
- collecte et structuration des données,
- programmation orientée objet,
- analyse textuelle,
- moteur de recherche,
- interface utilisateur sous forme de notebook.

---

## Contenu du projet

### 📂 Fichiers principaux

- `Author.py`  
  Classe représentant un auteur et sa production.

- `Document.py`  
  Classe de base `Document` et classes filles pour les différents types de documents.

- `Corpus.py` / `CorpusSingleton.py`  
  Gestion du corpus (stockage, ajout de documents, statistiques, méthodes d’analyse).

- `SearchEngine.py`  
  Implémentation du moteur de recherche (TF, TF-IDF, similarité cosinus).

- `interface.ipynb`  
  Notebook contenant l’interface graphique interactive (widgets).

- `data/corpus.csv`  
  Fichier CSV contenant le corpus final utilisé par l’interface.

---

## Corpus


- Sources :
  - **Reddit** (discussions, posts)
  - **Arxiv** (articles scientifiques)
- Auteurs :
  - pseudos Reddit
  - auteurs scientifiques (Arxiv)

Le corpus est volontairement de taille réduite afin de faciliter l’exploration et la lisibilité des résultats, tout en conservant une structure cohérente.

---

## Fonctionnalités

### TD3 – Statistiques du corpus
- Taille du corpus
- Statistiques par source
- Nombre d’auteurs

### TD4 – Structuration et affichage
- Organisation des documents
- Tri et affichage des métadonnées
- Sauvegarde du corpus

### TD5 – Programmation orientée objet
- Héritage (`Document` et classes spécialisées)
- Singleton pour le corpus
- Factory pour la création de documents

### TD6 – Analyse textuelle
- Nettoyage et tokenisation
- Expressions régulières
- Statistiques TF / DF
- Concordances

### TD7 – Moteur de recherche
- Construction manuelle des matrices TF et TF-IDF
- Similarité cosinus
- Recherche par mots-clés avec classement des documents

### TD8 à TD10 – Interface graphique
Une interface interactive réalisée avec `ipywidgets` permet :

- **Stats** : visualisation des statistiques globales
- **Recherche** : recherche par mots-clés avec filtres
- **Comparaison** : comparaison lexicale entre sources + tableau TF/DF global
- **Temps** : évolution temporelle de la fréquence d’un mot
- **Auteurs** : exploration des documents par auteur

L’interface gère les cas limites (requête vide, aucun résultat, filtres incompatibles) et ne plante pas.



