"""Vérifications de schéma sur les .gpkg du projet Accessibilité MRN/SERM.

Lève les points laissés ouverts dans `MCD_MPD_accessibilite.md` (section
« À vérifier avant écriture du DDL réel ») sans nécessiter de base PostGIS :
lecture directe des GeoPackage via geopandas. Produit un rapport Markdown,
pas de sortie binaire, pour rester déposable tel quel dans les Project
Files ou collable dans le chat.

Usage :
    python verifier_gpkg_accessibilite.py --dossier /chemin/vers/les/gpkg

Les neuf fichiers sont attendus avec leur nom d'origine
(`arrets_2026.gpkg`, `isochrones_SERM.gpkg`, etc.) dans `--dossier`.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd
import pandas as pd


def tableau_markdown(df: pd.DataFrame) -> str:
    """Rendu Markdown minimal d'un DataFrame, sans dépendre de `tabulate`.

    Équivalent suffisant à `DataFrame.to_markdown()` pour les tableaux
    simples produits par ce script (pas de fusion de cellules, pas
    d'alignement décimal fin) - évite d'ajouter une dépendance pour un
    script de vérification ponctuel.
    """
    colonnes = [str(c) for c in df.columns]
    lignes_donnees = [[str(v) for v in ligne] for ligne in df.itertuples(index=False)]
    entete = "| " + " | ".join(colonnes) + " |"
    separateur = "| " + " | ".join("---" for _ in colonnes) + " |"
    corps = "\n".join("| " + " | ".join(l) + " |" for l in lignes_donnees)
    return "\n".join([entete, separateur, corps])


def verifier_unicite(
    gdf: gpd.GeoDataFrame, colonnes: list[str], nom_table: str
) -> str:
    """Vérifie l'unicité d'une combinaison de colonnes, retourne un bloc Markdown."""
    doublons = gdf.groupby(colonnes, dropna=False).size().rename("n_occurrences")
    doublons = doublons[doublons > 1]
    lignes = [f"### Unicité `{colonnes}` sur `{nom_table}`", ""]
    if doublons.empty:
        lignes.append(
            f"Unique confirmé : {len(gdf):,} lignes, aucune combinaison "
            f"répétée sur {colonnes}."
        )
    else:
        lignes.append(
            f"**Non unique** : {len(doublons)} combinaison(s) répétée(s) "
            f"sur {len(gdf):,} lignes. Exemples (5 premiers) :"
        )
        lignes.append("")
        lignes.append(tableau_markdown(doublons.head(5).reset_index()))
    lignes.append("")
    return "\n".join(lignes)


def comparer_arrets(gdf_2026: gpd.GeoDataFrame, gdf_serm: gpd.GeoDataFrame) -> str:
    """Compare les id_source entre horizons : inchangés / nouveaux / incohérents.

    Robuste aux id_source dupliqués *au sein d'un même fichier* (ex. un
    arrêt desservi par plusieurs lignes, une ligne par ligne desservie) :
    la comparaison attribut par attribut n'est faite que sur les
    id_source strictement uniques dans les deux fichiers - les autres
    sont comptés séparément plutôt que de faire planter la comparaison.
    """
    dup_2026 = int(gdf_2026["id_source"].duplicated(keep=False).sum())
    dup_serm = int(gdf_serm["id_source"].duplicated(keep=False).sum())

    ids_2026 = set(gdf_2026["id_source"])
    ids_serm = set(gdf_serm["id_source"])
    communs = ids_2026 & ids_serm
    nouveaux_serm = ids_serm - ids_2026
    disparus = ids_2026 - ids_serm

    # Comparaison attribut par attribut : uniquement sur les id_source
    # uniques dans les DEUX fichiers, pour éviter l'ambiguïté d'un
    # .loc[id_source] qui retournerait plusieurs lignes.
    uniques_2026 = set(
        gdf_2026.loc[~gdf_2026["id_source"].duplicated(keep=False), "id_source"]
    )
    uniques_serm = set(
        gdf_serm.loc[~gdf_serm["id_source"].duplicated(keep=False), "id_source"]
    )
    communs_comparables = communs & uniques_2026 & uniques_serm
    communs_non_comparables = communs - communs_comparables

    colonnes_comparees = [
        c for c in ("nom", "mode", "lignes", "operateur") if c in gdf_2026.columns
    ]
    a = gdf_2026.set_index("id_source")
    b = gdf_serm.set_index("id_source")
    incoherents = []
    for id_source in communs_comparables:
        ligne_a, ligne_b = a.loc[id_source], b.loc[id_source]
        attrs_diff = any(ligne_a[c] != ligne_b[c] for c in colonnes_comparees)
        geom_diff = not ligne_a.geometry.equals_exact(ligne_b.geometry, tolerance=0.01)
        if attrs_diff or geom_diff:
            incoherents.append(id_source)

    remarque_2026 = (
        " - id_source n'est donc pas une clé naturelle unique par arrêt, "
        "à revoir dans le MCD (clé composite ou surrogate)"
        if dup_2026
        else ""
    )
    remarque_serm = " - même remarque" if dup_serm else ""

    lignes = [
        "### Comparaison `arrets_2026` / `arrets_SERM`",
        "",
        f"- `id_source` dupliqué au sein de `arrets_2026` : {dup_2026:,} ligne(s) "
        f"concernée(s){remarque_2026}",
        f"- `id_source` dupliqué au sein de `arrets_SERM` : {dup_serm:,} ligne(s) "
        f"concernée(s){remarque_serm}",
        f"- Arrêts communs aux deux horizons : {len(communs):,}, dont "
        f"{len(communs_comparables):,} comparables attribut par attribut "
        f"(id_source unique des deux côtés) et {len(communs_non_comparables):,} "
        f"non comparables automatiquement (id_source dupliqué d'au moins un côté "
        f"- à examiner manuellement)",
        f"- Arrêts uniquement en SERM (nouveaux, `horizon_apparition='SERM'`) : "
        f"{len(nouveaux_serm):,}",
        f"- Arrêts en 2026 absents de SERM (à examiner - suppression de "
        f"service ?) : {len(disparus):,}",
        f"- Parmi les {len(communs_comparables):,} comparables, incohérents "
        f"(attributs ou géométrie différents malgré même `id_source`) : "
        f"{len(incoherents)}",
    ]
    if incoherents:
        lignes.append("")
        lignes.append(f"  Exemples : {incoherents[:10]}")
    lignes.append("")
    return "\n".join(lignes)


def inventaire_colonnes(gdf: gpd.GeoDataFrame, nom_table: str) -> str:
    """Liste complète des colonnes et types, pour combler les colonnes hors du head."""
    lignes = [f"### Inventaire complet des colonnes - `{nom_table}`", ""]
    df_types = pd.DataFrame(
        {"colonne": gdf.columns, "type": [str(t) for t in gdf.dtypes]}
    )
    lignes.append(tableau_markdown(df_types))
    lignes.append("")
    lignes.append(f"{len(gdf):,} lignes.")
    lignes.append("")
    return "\n".join(lignes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dossier",
        type=Path,
        required=True,
        help="Dossier contenant les neuf .gpkg du projet Accessibilité",
    )
    parser.add_argument(
        "--sortie",
        type=Path,
        default=Path("rapport_verification_gpkg.md"),
        help="Fichier Markdown de sortie",
    )
    args = parser.parse_args()

    rapport = ["# Rapport de vérification - .gpkg Accessibilité MRN/SERM", ""]

    # 1. Isochrones : unicité (mode_deplacement, niveau, tranche_min, horizon)
    iso_2026 = gpd.read_file(args.dossier / "isochrones_2026.gpkg")
    iso_serm = gpd.read_file(args.dossier / "isochrones_SERM.gpkg")
    isochrones = pd.concat([iso_2026, iso_serm], ignore_index=True)
    rapport.append(
        verifier_unicite(
            isochrones,
            ["mode_deplacement", "niveau", "tranche_min", "horizon"],
            "isochrones (2026 + SERM)",
        )
    )

    # 2. Accès aux nœuds : unicité (node, mode_deplacement, niveau, horizon)
    acc_2026 = gpd.read_file(args.dossier / "acces_noeuds_2026.gpkg")
    acc_serm = gpd.read_file(args.dossier / "acces_noeuds_SERM.gpkg")
    acces = pd.concat([acc_2026, acc_serm], ignore_index=True)
    rapport.append(
        verifier_unicite(
            acces,
            ["node", "mode_deplacement", "niveau", "horizon"],
            "acces_noeuds (2026 + SERM)",
        )
    )

    # 3. Arrêts : comparaison id_source entre horizons
    arr_2026 = gpd.read_file(args.dossier / "arrets_2026.gpkg")
    arr_serm = gpd.read_file(args.dossier / "arrets_SERM.gpkg")
    rapport.append(comparer_arrets(arr_2026, arr_serm))

    # 4. Population : inventaire complet des colonnes (au-delà du head)
    pop = gpd.read_file(args.dossier / "population_carreaux_MRN.gpkg")
    rapport.append(inventaire_colonnes(pop, "population_carreaux_MRN"))

    args.sortie.write_text("\n".join(rapport), encoding="utf-8")
    print(f"Rapport écrit : {args.sortie.resolve()}")


if __name__ == "__main__":
    main()
