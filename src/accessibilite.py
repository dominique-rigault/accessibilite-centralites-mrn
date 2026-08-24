"""Fonctions de calcul d'atteignabilité, communes aux notebooks `03` et `05`.

Extraites des notebooks pour éviter la duplication de la logique de calcul
entre le notebook qui produit les isochrones (`03`) et celui qui les exploite
au niveau des carreaux de population (`05`).
"""

import math
from collections import defaultdict

import networkx as nx

from src.parametres import PAS_TRANCHE_MIN


def atteignabilite(G, noeud_origine, cutoff):
    """Temps d'accès continu (minutes) de chaque nœud atteignable depuis
    `noeud_origine`, via un unique Dijkstra à seuil. La conversion en tranche
    (5 / 10 / 15) est dérivée en aval par `tranche_de` : le temps continu
    (nécessaire à la correction du tronçon d'approche en nb05) n'est plus perdu.
    """
    return nx.single_source_dijkstra_path_length(
        G, noeud_origine, cutoff=cutoff, weight="temps"
    )


def tranche_de(t, pas=PAS_TRANCHE_MIN):
    """Tranche (multiple de `pas`) couvrant le temps continu `t`.
    L'origine (t = 0) est classée en première tranche.
    """
    return max(pas, pas * math.ceil(t / pas))


def construire_index(gdf_acces):
    """Construit un dict (mode_deplacement, node) → liste de
    (niveau_ordre, temps_acces_s) depuis la table `acces_noeuds` d'un horizon.
    Permet la lecture O(1) par nœud (nb05).
    """
    idx = defaultdict(list)
    for _, row in gdf_acces.iterrows():
        idx[(row["mode_deplacement"], row["node"])].append(
            (row["niveau_ordre"], row["temps_acces_s"])
        )
    return idx


def meilleur_niveau_depuis_noeud(node, mode, budget_s, idx):
    """Meilleur niveau_ordre atteignable depuis `node` sous `budget_s` secondes.
    Retourne 0 si aucun niveau n'est atteignable.
    """
    entrees = idx.get((mode, node), [])
    atteignables = [niv for niv, t in entrees if t <= budget_s]
    return max(atteignables, default=0)


def pop_atteignant_niveau(df, mode, niveau_min, col_niveau):
    """Population (ind_pond) atteignant au moins `niveau_min` pour le mode donné."""
    masque = (df["mode"] == mode) & (df[col_niveau] >= niveau_min)
    return df.loc[masque, "ind_pond"].sum()


def pop_exactement_niveau(df, mode, niveau_exact, col_niveau):
    """Population (ind_pond) atteignant exactement `niveau_exact` pour le mode donné."""
    masque = (df["mode"] == mode) & (df[col_niveau] == niveau_exact)
    return df.loc[masque, "ind_pond"].sum()


def aire_structurante(iso, mode_dep, tranche, structurants):
    """Aire (km²) de l'emprise structurante pour un mode et une tranche donnés,
    tous niveaux structurants confondus (union des géométries).
    """
    sel = iso[
        (iso["mode_deplacement"] == mode_dep)
        & (iso["tranche_min"] == tranche)
        & (iso["niveau"].isin(structurants))
    ]
    return sel.geometry.union_all().area / 1e6
