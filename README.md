# search_project

Projet Python (TD3 à TD7) : manipulation d’un corpus de documents (Reddit + Arxiv), statistiques, sauvegarde/chargement, concordance, TF/DF, et moteur de recherche TF-IDF.

## Structure
- `main.py` : menu console pour lancer TD3 → TD7
- `Corpus.py` : gestion du corpus + méthodes (stats, tri, sauvegarde, concat, etc.)
- `CorpusSingleton.py` : singleton basé sur `Corpus`
- `Document.py` / `DocumentFactory.py` : documents et création (Reddit/Arxiv)
- `Author.py` : gestion des auteurs
- `SearchEngine.py` : TD6/TD7 (regex, concordance, TF/DF, TF-IDF)


