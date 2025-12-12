import math
import re
import pandas as pd
from collections import defaultdict


class SearchEngine:
    def __init__(self, corpus):
        self.corpus = corpus
        self.index = None
        self.idf = {}
        self.doc_norms = {}

    # ===== TD6 =====

    def nettoyer_texte(self, texte: str) -> str:
        if not texte:
            return ""
        t = texte.lower()
        t = t.replace("\n", " ")
        t = re.sub(r"[^a-z0-9\s]", " ", t)
        t = re.sub(r"\s+", " ", t)
        return t.strip()

    def search_regex(self, pattern: str):
        chaine = self.corpus.chaine_concatenee()
        return [m.group() for m in re.finditer(pattern, chaine)]

    def concorde(self, pattern: str, contexte: int = 30):
        lignes = []
        for doc in self.corpus.id2doc.values():
            texte = doc.texte or ""
            for m in re.finditer(pattern, texte, flags=re.IGNORECASE):
                debut = max(0, m.start() - contexte)
                fin = min(len(texte), m.end() + contexte)
                lignes.append({
                    "contexte_gauche": texte[debut:m.start()],
                    "motif": texte[m.start():m.end()],
                    "contexte_droit": texte[m.end():fin],
                })
        return pd.DataFrame(lignes)

    def construire_vocabulaire(self):
        tf_global = defaultdict(int)
        df = defaultdict(int)

        for doc in self.corpus.id2doc.values():
            texte = self.nettoyer_texte(doc.texte or "")
            mots = texte.split()
            vus = set()
            for mot in mots:
                tf_global[mot] += 1
                if mot not in vus:
                    df[mot] += 1
                    vus.add(mot)

        data = [{"mot": m, "TF": tf_global[m], "DF": df[m]} for m in tf_global]
        return pd.DataFrame(data).sort_values("TF", ascending=False)

    # ===== TD7 =====

    def construire_index(self):
        index = defaultdict(lambda: defaultdict(int))
        df = defaultdict(int)

        for doc_id, doc in self.corpus.id2doc.items():
            texte = self.nettoyer_texte(doc.texte or "")
            mots = texte.split()
            vus = set()
            for mot in mots:
                index[mot][doc_id] += 1
                if mot not in vus:
                    df[mot] += 1
                    vus.add(mot)

        n_docs = self.corpus.ndoc
        self.idf = {
            mot: math.log((1 + n_docs) / (1 + df_mot)) + 1
            for mot, df_mot in df.items()
        }

        self.doc_norms = defaultdict(float)
        for mot, postings in index.items():
            for doc_id, tf in postings.items():
                w = tf * self.idf[mot]
                self.doc_norms[doc_id] += w * w

        for d in self.doc_norms:
            self.doc_norms[d] = math.sqrt(self.doc_norms[d])

        self.index = index

    def search(self, requete: str, k: int = 5):
        if self.index is None:
            self.construire_index()

        texte = self.nettoyer_texte(requete)
        if not texte:
            return pd.DataFrame()

        q_tf = defaultdict(int)
        for mot in texte.split():
            if mot in self.idf:
                q_tf[mot] += 1

        q_vec = {m: q_tf[m] * self.idf[m] for m in q_tf}
        q_norm = math.sqrt(sum(v*v for v in q_vec.values()))
        if q_norm == 0:
            return pd.DataFrame()

        scores = defaultdict(float)
        for mot, q_val in q_vec.items():
            for doc_id, tf in self.index.get(mot, {}).items():
                scores[doc_id] += (tf * self.idf[mot]) * q_val

        results = []
        for doc_id, score in scores.items():
            d_norm = self.doc_norms.get(doc_id, 1)
            score = score / (d_norm * q_norm)
            doc = self.corpus.id2doc[doc_id]
            results.append({
                "score": round(score, 4),
                "id": doc_id,
                "titre": doc.titre,
                "auteur": doc.auteur,
            })

        return pd.DataFrame(results).sort_values("score", ascending=False).head(k)
