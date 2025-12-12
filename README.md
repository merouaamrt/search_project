# – Version 1 (TD3–TD5)

## Description
Cette version correspond aux TD3 à TD5 du projet
Elle met en place la structure orientée objet du projet ainsi que la gestion
d’un corpus de documents textuels issus de Reddit et d’arXiv.

## Fonctionnalités implémentées

### TD3 – Modélisation orientée objet
- Classe `Document` (classe mère)
- Spécialisations `RedditDocument` et `ArxivDocument`
- Classe `Author`
- Classe `Corpus` pour la gestion des documents et des auteurs

### TD4 – Manipulation du corpus
- Chargement d’un corpus de documents
- Calcul de statistiques (mots, phrases, caractères)
- Concaténation du corpus en une chaîne unique
- Tri des documents (par titre, par date)
- Sauvegarde et rechargement du corpus au format CSV

### TD5 – Design Patterns
- Implémentation du pattern **Singleton** pour le corpus
- Implémentation du pattern **Factory** pour la création des documents



