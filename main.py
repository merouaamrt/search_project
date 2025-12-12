from CorpusSingleton import CorpusSingleton
from Corpus import Corpus
from DocumentFactory import DocumentFactory
import praw
import urllib.request, urllib.parse
import xmltodict
import os
from SearchEngine import SearchEngine


# True = récupérer les données depuis les APIs Reddit/Arxiv
# False = charger depuis un CSV déjà existant

RECUPERER_DEPUIS_API = False

def recuperer_donnees():
    """
    Récupère les données depuis Reddit et Arxiv et les stocke dans le Corpus Singleton.
    """
    corpus = CorpusSingleton("AI Research")

    # --- Récupération des posts Reddit ---
    try:
        reddit = praw.Reddit(
            client_id="jKeuB_dHOvdpwiJNCLs7xg",
            
            client_secret="ZcOEh1YFKEAKEZ5CfcIf821AYwufBg",
            user_agent="P_IA (by u/Sure_Map_8580)"
        )

        theme = "artificial intelligence"

        for post in reddit.subreddit("all").search(theme, limit=10):
            
            texte = (post.title + " " + post.selftext).replace("\n", " ")
            auteur = str(post.author) if post.author else "Inconnu"
            

            # Crée un document Reddit et l’ajoute au corpus
            doc = DocumentFactory.create_document(
                source="Reddit",
                titre=post.title,
                auteur_or_auteurs=auteur,
                
                date=post.created_utc,
                
                url=post.url,
                texte=texte,
                nb_commentaires=post.num_comments
                
            )
            corpus.ajouter_document(doc)
    except Exception as e:
        print(f"Erreur lors de la récupération Reddit : {e}")

    # --- Récupération des articles Arxiv ---
    try:
        theme_encoded = urllib.parse.quote(theme)
        url = f"http://export.arxiv.org/api/query?search_query=all:{theme_encoded}&start=0&max_results=5"

        with urllib.request.urlopen(url) as response:
            data = response.read()

        feed = xmltodict.parse(data)
        entries = feed["feed"]["entry"]
        if isinstance(entries, dict):
            
            entries = [entries]

        for entry in entries:
            texte = entry["summary"].replace("\n", " ")
            authors = entry["author"]

            # Gère le cas auteur unique ou multiple
            if isinstance(authors, dict):
                liste_auteurs = [authors["name"]]
            else:
                liste_auteurs = [a["name"] for a in authors]

            # Crée un document Arxiv et l’ajoute au corpus
            doc = DocumentFactory.create_document(
                source="Arxiv",
                titre=entry["title"],
                auteur_or_auteurs=liste_auteurs,
                date=entry["published"],
                url=entry["id"],
                texte=texte
            )
            corpus.ajouter_document(doc)
            
    except Exception as e:
        
        print(f"Erreur lors de la récupération Arxiv : {e}")

    return corpus


def tests_td3(corpus):
    """
    Affiche les statistiques simples du corpus (TD3) :
    nombre de documents, taille, concaténation des textes.
    """
    corpus.afficher_stats_basiques()
    corpus.concatener_textes()


def tests_td4(corpus):
    """
    Montre l’utilisation des classes Document, Author et Corpus (TD4)
    """
    if corpus.ndoc > 0:
        premier = list(corpus.id2doc.values())[0]
        print("Exemple de document :")
        print(premier)
        premier.afficher_infos()

    print(f"Nombre d’auteurs : {corpus.naut}")
    print("Quelques documents triés par titre :")
    corpus.afficher_par_titre(5)
    print("Quelques documents triés par date :")
    corpus.afficher_par_date(5)

    # Sauvegarde et rechargement pour tester la persistance
    corpus.save("data/corpus_test.csv")
    corpus_test = Corpus.load("data/corpus_test.csv")
    print("Corpus rechargé :")
    print(corpus_test)


def tests_td5(corpus):
    """
    Montre l’héritage et les design patterns (TD5) :
    - RedditDocument, ArxivDocument
    - Singleton
    - Factory
    """
    print("Exemples de documents :")
    for doc in list(corpus.id2doc.values())[:5]:
        print(doc)
        if hasattr(doc, "nb_commentaires"):
            print(f"Commentaires : {doc.getNbCommentaires()}")
        if hasattr(doc, "auteurs"):
            print(f"Auteurs : {', '.join(doc.getCoAuteurs())}")

    # Vérification du singleton
    corpus2 = CorpusSingleton("X")
    print(f"Singleton fonctionne ? {corpus is corpus2}")

    # Exemple de création via Factory
    doc_test = DocumentFactory.create_document(
        source="Reddit",
        titre="Test",
        auteur_or_auteurs="Author",
        date=0,
        url="http://test.com",
        texte="Ceci est un document test",
        nb_commentaires=1
    )
    print("Document créé via Factory :", doc_test)
    
def tests_td6(corpus):
    moteur = corpus.search_engine

    print("\n===== TESTS TD6 =====\n")

    motif = input("Motif à rechercher (regex) : ").strip()
    if not motif:
        print("Motif vide. Retour au menu.")
        return

    matches = moteur.search_regex(motif)
    print(f"\nNombre d'occurrences trouvées : {len(matches)}")

    choix = input("Afficher la concordance ? (o/n) : ").strip().lower()
    if choix == "o":
        concorde_df = moteur.concorde(motif)
        print("\nConcordance (5 premières lignes) :")
        print(concorde_df.head())

    choix = input("Afficher les statistiques TF/DF ? (o/n) : ").strip().lower()
    if choix == "o":
        table = moteur.construire_vocabulaire()
        print("\nTop 10 des mots les plus fréquents :")
        print(table.head(10))


def tests_td7(corpus):
    moteur = corpus.search_engine

    print("\n===== TESTS TD7 : MOTEUR DE RECHERCHE =====\n")

    while True:
        requete = input("Requête (vide pour revenir au menu) : ").strip()
        if not requete:
            break

        k_str = input("Nombre de documents à afficher (défaut 5) : ").strip()
        try:
            k = int(k_str) if k_str else 5
        except ValueError:
            print("Nombre invalide.")
            continue

        resultats = moteur.search(requete, k)

        if resultats.empty:
            print("\nAucun document trouvé.\n")
            continue

        print("\nRésultats :\n")
        for _, row in resultats.iterrows():
            print(f"- [score={row['score']}] {row['titre']} – {row['auteur']}")


def menu(corpus):
    while True:
        print("\n========= MENU =========")
        print("0 - TD3 : statistiques du corpus")
        print("1 - TD4 : tri, affichage, sauvegarde")
        print("2 - TD5 : héritage, singleton, factory")
        print("3 - TD6 : regex, concordance, stats TF/DF")
        print("4 - TD7 : moteur de recherche")
        print("5 - Quitter")

        choix = input("Votre choix : ").strip()

        if choix == "0":
            tests_td3(corpus)
        elif choix == "1":
            tests_td4(corpus)
        elif choix == "2":
            tests_td5(corpus)
        elif choix == "3":
            tests_td6(corpus)
        elif choix == "4":
            tests_td7(corpus)
        elif choix == "5":
            print("\n👋 Fin du programme.")
            break
        else:
            print("Choix invalide.")

def main():
    if not os.path.exists("data"):
        os.makedirs("data")

    # Chargement ou récupération des données
    if RECUPERER_DEPUIS_API:
        corpus = recuperer_donnees()
        corpus.save("data/corpus.csv")
    else:
        if os.path.exists("data/corpus.csv"):
            corpus = CorpusSingleton("AI Research")
            temp = Corpus.load("data/corpus.csv")
            corpus.id2doc = temp.id2doc
            corpus.authors = temp.authors
            corpus.ndoc = temp.ndoc
            corpus.naut = temp.naut
        else:
            corpus = recuperer_donnees()
            corpus.save("data/corpus.csv")

    
    menu(corpus)


    # Résumé final
    print(f"{corpus.ndoc} documents, {corpus.naut} auteurs")


if __name__ == "__main__":
    main()
