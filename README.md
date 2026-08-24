# Accessibilité bas carbone aux centralités
## Métropole Rouen Normandie · Impact du SERM

Analyse de l'accessibilité piétonne et cyclable aux réseaux de transports 
en commun structurants, comparée entre la situation actuelle et le réseau 
cible du Service Express Régional Métropolitain (SERM).

> **Statut du projet.** Analyse personnelle menée pour démontrer une
> méthode, à l'appui de futures missions du même type; non commanditée par
> la Métropole Rouen Normandie ni par la Société des Grands Projets, dont
> les données publiques servent ici de cas d'application. La méthode est
> détaillée dans [`docs/methode.md`](docs/methode.md), rédigée pour rester
> transposable à un autre territoire.

## Question analytique

> Pour chaque lieu d'habitation, quel est le meilleur niveau de desserte 
> en transport en commun structurant atteignable en moins de 15 minutes 
> à pied ou à vélo, et quelle part de la population voit ce niveau s'élever 
> avec le réseau cible SERM ?

**Indicateur retenu.** L'accès binaire à un arrêt *quelconque* est saturé à
l'échelle de l'agglomération (presque tout habitant est à moins de 15 min d'un
arrêt) : il ne mesure pas ce que change le SERM, qui agit sur le réseau
structurant et non sur le maillage bus. L'indicateur est donc le **meilleur
niveau de desserte structurante atteignable** à pied ou à vélo, ordonné par
portée croissante :

`aucun < bus < TEOR < métro < car express < train`

La lecture avant / après mesure le nombre d'habitants dont ce niveau s'élève
avec le réseau cible SERM. Les temps de parcours sont restitués en gradient
(5 / 10 / 15 min) plutôt qu'à un seuil unique. Le bac, structurant sur son seul
corridor et marginal en population, est exclu de la hiérarchie.

**Périmètres d'analyse.** Deux périmètres sont distingués : l'*offre* (réseaux
viaires + arrêts) est étendue à la MRN augmentée d'un tampon +3 750 m pour les
arrêts (15 min à vélo), +5 000 m pour les graphes viaires, afin de capter les
arrêts hors MRN plus proches d'un habitant qu'un arrêt interne; la *demande*
(population Filosofi) reste circonscrite à la MRN stricte.

## Cadrage

Ce projet s'inscrit en cohérence avec le Plan de Mobilité (PDM) de la 
Métropole Rouen Normandie et avec le réseau cible du SERM, dont la 
préfiguration (confiée à la Société des Grands Projets) a été engagée en 
septembre 2024. À la date de l'analyse, le réseau cible (volet ferroviaire et 
car express) est défini dans les documents techniques publics, dont la 
délibération du Conseil métropolitain du 15 décembre 2025, mais son phasage 
opérationnel n'est pas arrêté : l'analyse retient donc le réseau cible complet 
comme terme de comparaison, et non un état daté.

Le document de cadrage complet est disponible dans [`docs/`](docs/).

**À qui s'adresse l'analyse, et pour décider quoi.** L'accessibilité mesurée
ici n'est pas une fin en soi : elle supporte les arbitrages de l'autorité
organisatrice de la mobilité (Métropole Rouen Normandie), des aménageurs et de
l'observatoire de la mobilité. Concrètement, elle éclaire trois décisions : où
concentrer le rabattement vers les futures haltes SERM (bus, modes actifs,
stationnement vélo), quels secteurs habités resteront mal desservis malgré le
réseau cible SERM, et comment objectiver l'équité territoriale d'accès au réseau
structurant.

## Stack technique

`Python` `GeoPandas` `OSMnx` `Folium` `QGIS` `Jupyter`

## Sources de données

- Réseaux viaires piétons et cyclables : OpenStreetMap (OSMnx)
- Réseaux TC : [transport.data.gouv.fr](https://transport.data.gouv.fr/datasets/region/28?subtype=intercity&type=public-transit)
- Population et logements : INSEE Filosofi carroyé 200 m
- Haltes du réseau cible SERM (ferroviaire post-LNPN, car express) : délibération du Conseil métropolitain 15/12/2025 et schémas de préfiguration
- Armature urbaine :
    Fichier des 71 communes de la MRN avec leur type de centralité.
    **Sources** :
    Liste des communes : [COG data.gouv.fr](https://www.data.gouv.fr/datasets/code-officiel-geographique-cog)
    Types de centralité : PAS Métropole Rouen Normandie 2050, carte n°4
    **Méthode** : enrichissement manuel du COG
    Ce fichier ne peut pas être régénéré automatiquement.

## Installation et exécution

**Prérequis** : Python 3.11 ou supérieur, un environnement virtuel dédié
(`venv` ou `conda`), une connexion internet (API Nominatim / OpenStreetMap,
notebook `00`).

1. **Cloner le dépôt et installer les dépendances** :
   ```bash
   git clone https://github.com/dominique-rigault/accessibilite-centralites-mrn.git
   cd accessibilite-centralites-mrn
   python -m venv .venv
   ```
   Activation de l'environnement virtuel, selon la plateforme :
   ```bash
   # macOS / Linux
   source .venv/bin/activate
   ```
   ```powershell
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   ```
   Puis, dans tous les cas :
   ```bash
   pip install -e .
   ```
   L'installation en mode éditable (`-e .`) rend le package `src/` importable
   depuis les notebooks, quel que soit le répertoire de travail effectif de
   Jupyter ou de l'éditeur utilisé.

2. **Placer les données brutes non versionnées** dans `raw/` :

   | Fichier | Source |
   |---|---|
   | `atoumod-gtfs_20260512/` (dossier GTFS) | [transport.data.gouv.fr](https://transport.data.gouv.fr/datasets/region/28?subtype=intercity&type=public-transit) |
   | `Filosofi2021_carreaux_200m_csv.zip` | [INSEE Filosofi carroyé 200 m](https://www.insee.fr/fr/statistiques/7655475) |

   Et dans `data/` :

   | Fichier | Source |
   |---|---|
   | `armature_urbaine.csv` | Enrichissement manuel du COG (types de centralité, PAS Métropole Rouen Normandie 2050 carte n°4), ne peut pas être régénéré automatiquement |
   | `Arrets_SERM.xlsx` | Géolocalisation manuelle des haltes SERM depuis la délibération du Conseil métropolitain du 15/12/2025 et les schémas de préfiguration, ne peut pas être régénéré automatiquement |

   Les autres fichiers de `data/` sont produits par la chaîne elle-même.

3. **Exécuter les notebooks dans l'ordre du tableau ci-dessous.** Le notebook
   `03` est paramétré par `HORIZON` (`"2026"` puis `"SERM"`) : l'exécuter une
   fois pour chaque valeur avant de lancer `05`.

## Pipeline analytique

Traitements organisés en notebooks numérotés, à exécuter dans l'ordre.
`00` produit les référentiels transversaux; `01` et `02` en dépendent
mais sont indépendants l'un de l'autre. Les graphes viaires (`01`) et la
population (`04`) sont identiques pour les deux horizons; seuls les arrêts
(`02`) et les isochrones / atteignabilité (`03`) sont déclinés par horizon
(situation actuelle, réseau cible SERM).

| Notebook | Rôle | Sortie principale |
|----------|------|-------------------|
| `00_referentiels.ipynb` | Périmètre administratif de la MRN (géocodage OSM) | `data/perimetre_MRN.gpkg` |
| `01_acquisition_donnees_OSM.ipynb` | Réseaux viaires piéton et cyclable (OSMnx), périmètre offre (MRN + tampon 5 km) | `data/reseau_{pieton,velo}_MRN.gpkg` + `.graphml` |
| `02_arrets_TC.ipynb` | Couches d'arrêts : situation actuelle depuis le GTFS ATOUMOD, puis réseau cible SERM par overlay (haltes ferroviaires post-LNPN, car express, nouveaux arrêts TEOR, géolocalisés manuellement). Périmètre offre (MRN + tampon 3,75 km), attribut de niveau de desserte | `data/arrets_2026.gpkg` + `data/arrets_SERM.gpkg` |
| `03_isochrones.ipynb` | Isochrones piétonnes et cyclables en routage réel depuis les arrêts (niveau de desserte conservé), et table du meilleur niveau atteignable par nœud (niveau de desserte et temps d'accès). Traitement paramétré par horizon, exécuté pour la situation actuelle et le réseau cible | `data/isochrones_{2026,SERM}.gpkg` + `data/acces_noeuds_{2026,SERM}.gpkg` |
| `04_logements.ipynb` | Couche de population localisée (Filosofi 200 m, découpe MRN stricte) | `data/population_carreaux_MRN.gpkg` |
| `05_logements_accessibilite.ipynb` | Rattachement des carreaux de population au réseau (snap-to-edge), lecture du meilleur niveau de desserte atteignable par carreau pour les deux horizons (`niveau_actuel`, `niveau_cible`), agrégats de population pondérés | `data/population_accessibilite_MRN.gpkg` |
| `06_comparaison_avant_apres.ipynb` *à venir* | Vue différentielle situation actuelle / réseau cible SERM : habitants gagnant un niveau de desserte | · |

> Chaque notebook documente en tête ses prérequis, entrées et sorties détaillés.

## Restitution & aide à la décision

Au-delà des cartes d'isochrones, l'analyse est construite pour produire une
lecture directement actionnable :

- **Part de population atteignant une desserte structurante (< 15 min), et
  niveau atteint, avant / après SERM** à l'échelle métropolitaine, puis par
  commune et par type de centralité : l'indicateur d'équité territoriale.
- **Secteurs habités en déficit d'accès malgré le réseau cible SERM** cartographie des
  zones où se posent les arbitrages de rabattement et d'aménagement.
- **Gain marginal du SERM** nombre d'habitants qui gagnent au moins un niveau
  de desserte grâce aux nouvelles haltes, pour objectiver l'apport du projet.

Forme de la recommandation visée : *« prioriser [tel aménagement] sur [tel
secteur], qui ramène le plus d'habitants aujourd'hui mal desservis sous le seuil
d'accessibilité, au meilleur rapport coût / population atteinte. »*

**Indicateurs nb05 (situation 2026 / réseau cible SERM, population Filosofi 453 k hab.) :**
à pied, 30,3 % de la population MRN gagne au moins un niveau de desserte structurante grâce au réseau cible SERM; à vélo, 32,3 %.
*(Agrégats par commune et par type de centralité, et indicateurs nb06, à compléter.)*

## Limites et domaine de validité

La note de limites destinée à un lecteur externe (portée de la méthode,
précision des sources, hypothèses simplificatrices, dépendance aux
référentiels externes vivants, conditions de transposition) est dans
[`docs/methode.md`](docs/methode.md#note-de-limites-et-domaine-de-validité).

Les points suivants complètent cette note avec le détail d'implémentation,
utile pour qui reprend ou audite le code plutôt que pour un lecteur du
livrable final :

- **Rattachement des arrêts au réseau (snap-to-node, nb03)** : chaque arrêt
  est routé depuis le nœud du graphe le plus proche, le tronçon d'approche
  n'étant ni routé ni décompté du budget-temps. Pour les modes structurants
  (Métro, TEOR, Train), qui portent l'indicateur, ce rattachement reste sous
  70 m dans tous les cas (médiane 15 m à pied, 23 m à vélo; p95 ≤ 50 m). Le
  maillage bus, hors hiérarchie, présente un arrêt isolé à 460 m
  (Le Conihout, Le Mesnil-sous-Jumièges, ligne 206), routé depuis une
  extrémité d'arête OSM longue et non subdivisée : sans incidence sur
  l'indicateur, le *snap-to-node* est donc conservé pour les arrêts.
- **Rattachement des carreaux au réseau (snap-to-edge, nb05)** : contrairement
  aux arrêts, chaque carreau de population est rattaché par son point
  représentatif (`representative_point`) à l'arête la plus proche plutôt
  qu'au nœud, parce que les carreaux sont bien plus nombreux et tombent
  fréquemment sur des arêtes longues en secteur rural. Le tronçon d'approche
  le long de l'arête est alors décompté du budget-temps grâce au temps
  d'accès continu porté par `acces_noeuds` (nb03).
- **Correction du tronçon d'approche (nb05)** : estimée depuis la distance
  orthogonale de snap, borne inférieure de la distance curviligne réelle
  jusqu'à l'extrémité de l'arête. La correction est donc légèrement
  optimiste, dans une mesure cohérente avec la précision du carroyage.
- **Densité uniforme sur les carreaux de bordure (nb05)** : les carreaux
  tronqués par la limite de la MRN voient leur population pondérée au
  prorata de la surface conservée (`ind_pond = ind × frac`), ce qui
  introduit une erreur systématique pour les carreaux dont la population
  est concentrée dans la partie exclue.
- **Validation croisée point-dans-polygone (nb05)** : la concordance entre
  le snap-to-edge et la méthode point-dans-polygone contre `isochrones_2026`
  est de 74,6 %. Les 25,4 % de divergences sont quasi exclusivement des
  carreaux dont le point représentatif est à plus de 50 m de toute arête
  atteinte, ce qui confirme la supériorité du snap-to-edge pour les carreaux
  éloignés des arêtes.
- **Traversées de bac exclues du réseau viaire** : les bacs sur la Seine
  (Duclair, Jumièges, La Bouille, Sahurs, Mesnil-sous-Jumièges) ne sont pas
  modélisés comme arêtes, leur fréquence discontinue étant incompatible avec
  l'hypothèse de déplacement continu du pipeline. L'accessibilité des
  secteurs riverains concernés est donc légèrement sous-estimée.
- **Périmètre exclu (extensions ultérieures)** : routage depuis les lieux de
  travail (base SIRENE); analyse multicritères PLUi / PDM / SERM; découpage
  du réseau cible en jalons datés, à traiter lorsque le calendrier de mise
  en service sera stabilisé.

## Structure du projet
```
├── src/              # Code partagé (chemins, paramètres, calculs d'accessibilité)
├── notebooks/        # Analyses et traitements
├── docs/             # Document de cadrage
├── data/             # Données traitées (non versionnées)
├── raw/              # Données brutes (non versionnées)
├── cache/            # Cache OSMnx (non versionné)
├── pyproject.toml    # Dépendances et installation éditable (`pip install -e .`)
└── requirements.txt  # Miroir des dépendances pour `pip install -r`
```

## Partenariats institutionnels envisagés

Ce projet s'inscrit en cohérence avec les travaux de l'AURBSE (Agence 
d'Urbanisme de la Région de Rouen et de l'Estuaire de la Seine), notamment 
l'observatoire OMMeR et le diagnostic du bassin de mobilité Cœur Vallée 
de Seine. Un échange est envisagé pour aligner les angles d'analyse avec 
les besoins de l'observatoire.

## Auteur

Dominique Rigault, analyste de données géospatiales  
[linkedin.com/in/dominiquerigault](https://linkedin.com/in/dominiquerigault) · 
[github.com/dominique-rigault](https://github.com/dominique-rigault)

## Licence

Données et code publiés sous licence ouverte, réutilisation libre avec attribution.
