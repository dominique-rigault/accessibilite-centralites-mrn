# Accessibilité bas carbone aux centralités
## Métropole Rouen Normandie — Impact du SERM 2030

Analyse de l'accessibilité piétonne et cyclable aux réseaux de transports 
en commun structurants, avant et après la mise en service du Service Express 
Régional Métropolitain (SERM) à l'horizon 2030.

## Question analytique

> Quelle part de la population métropolitaine accède depuis son lieu 
> d'habitation aux transports en commun en moins de 15 minutes à pied 
> ou à vélo, et comment le SERM modifie-t-il cette proportion ?

## Cadrage

Ce projet s'inscrit en cohérence avec le Plan de Mobilité (PDM) de la 
Métropole Rouen Normandie et la phase 2030 du SERM, dont la délibération 
d'adoption a été votée en Conseil métropolitain le 15 décembre 2025.

Le document de cadrage complet est disponible dans [`docs/`](docs/).

**À qui s'adresse l'analyse, et pour décider quoi.** L'accessibilité mesurée
ici n'est pas une fin en soi : elle supporte les arbitrages de l'autorité
organisatrice de la mobilité (Métropole Rouen Normandie), des aménageurs et de
l'observatoire de la mobilité. Concrètement, elle éclaire trois décisions : où
concentrer le rabattement vers les futures haltes SERM (bus, modes actifs,
stationnement vélo), quels secteurs habités resteront mal desservis malgré le
SERM 2030, et comment objectiver l'équité territoriale d'accès au réseau
structurant.

## Stack technique

`Python` `GeoPandas` `OSMnx` `Folium` `QGIS` `Jupyter`

## Sources de données

- Réseaux viaires piétons et cyclables : OpenStreetMap (OSMnx)
- Réseaux TC : [transport.data.gouv.fr](https://transport.data.gouv.fr/datasets/region/28?subtype=intercity&type=public-transit)
- Population et logements : INSEE FiLoSoFi carroyé 200 m
- Haltes SERM projetées : délibération du Conseil métropolitain 15/12/2025
- Armature urbaine :
    Fichier des 71 communes de la MRN avec leur type de centralité.
    **Sources** :
    Liste des communes : [COG data.gouv.fr](https://www.data.gouv.fr/datasets/code-officiel-geographique-cog)
    Types de centralité : PAS Métropole Rouen Normandie 2050, carte n°4
    **Méthode** : enrichissement manuel du COG
    Ce fichier ne peut pas être régénéré automatiquement.

## Pipeline analytique

Traitements organisés en notebooks numérotés, à exécuter dans l'ordre.
`00` produit les référentiels transversaux ; `01` et `02` en dépendent
mais sont indépendants l'un de l'autre.

| Notebook | Rôle | Sortie principale |
|----------|------|-------------------|
| `00_referentiels.ipynb` | Périmètre administratif de la MRN (géocodage OSM) | `data/perimetre_MRN.gpkg` |
| `01_acquisition_donnees_OSM.ipynb` | Réseaux viaires piéton et cyclable (OSMnx) | `data/reseau_{pieton,velo}_MRN.gpkg` + `.graphml` |
| `02_arrets_TC.ipynb` | Couche d'arrêts TC 2026 depuis le GTFS ATOUMOD | `data/arrets_2026.gpkg` |
| `03_isochrones.ipynb` *— à venir* | Isochrones piétonnes et cyclables en routage réel depuis les arrêts | — |
| `04_logements.ipynb` | Couche de population localisée (Filosofi 200 m, découpe MRN) | `data/population_carreaux_MRN.gpkg` |
| `05_jointure_logements_isochrones.ipynb` *— à venir* | Jointure spatiale population (carroyage 200 m) ↔ isochrones | — |
| `06_comparaison_avant_apres.ipynb` *— à venir* | Vue différentielle situation actuelle / SERM 2030 | — |

> Chaque notebook documente en tête ses prérequis, entrées et sorties détaillés.

## Restitution & aide à la décision

Au-delà des cartes d'isochrones, l'analyse est construite pour produire une
lecture directement actionnable :

- **Part de population desservie (< 15 min), avant / après SERM** — à l'échelle
  métropolitaine, puis par commune et par type de centralité : l'indicateur
  d'équité territoriale.
- **Secteurs habités en déficit d'accès malgré le SERM 2030** — cartographie des
  zones où se posent les arbitrages de rabattement et d'aménagement.
- **Gain marginal du SERM** — nombre d'habitants qui basculent sous le seuil des
  15 min grâce aux nouvelles haltes, pour objectiver l'apport du projet.

Forme de la recommandation visée : *« prioriser [tel aménagement] sur [tel
secteur], qui ramène le plus d'habitants aujourd'hui mal desservis sous le seuil
d'accessibilité, au meilleur rapport coût / population atteinte. »*

*(Indicateurs chiffrés à compléter à l'issue des notebooks `03`, `05` et `06`.)*

## Limites et données manquantes

- **Écart de population** : population fiscale Filosofi 2021 (453 k individus de ménages) inférieure d'environ 8 % à la population municipale 2021 (491 k), différence imputable au champ des ménages fiscaux — hors population des communautés — et dans une moindre mesure aux carreaux imputés et à l'hypothèse de densité uniforme pour les carreaux traversés par la limite de la MRN.
- **Précision du carroyage** : le carroyage INSEE de 200 m introduit une 
  erreur de localisation comprise entre 0 et 100 m, soit de 0 à 1,2 mn à 
  pied. L'utilisation de la BDNB (Base de Données Nationale des Bâtiments) 
  permettrait de réduire cette marge en localisant la population au bâtiment.
- **Haltes SERM 2030** : en l'absence de couche SIG officielle à ce stade, 
  les coordonnées des haltes projetées sont géolocalisées manuellement à 
  partir des documents techniques publics (délibération du 15/12/2025).
- **Périmètre exclu (extensions ultérieures)** :
    - routage depuis les lieux de travail (base SIRENE) ;
    - analyse multicritères PLUi / PDM / SERM ;
    - horizons SERM pré-LNPN et post-LNPN, à traiter lorsque les données 
      de desserte seront stabilisées.

## Structure du projet
```
├── notebooks/        # Analyses et traitements
├── docs/             # Document de cadrage
├── data/             # Données traitées (non versionnées)
├── raw/              # Données brutes (non versionnées)
└── cache/            # Cache OSMnx (non versionné)
```

## Partenariats institutionnels envisagés

Ce projet s'inscrit en cohérence avec les travaux de l'AURBSE (Agence 
d'Urbanisme de la Région de Rouen et de l'Estuaire de la Seine), notamment 
l'observatoire OMMeR et le diagnostic du bassin de mobilité Cœur Vallée 
de Seine. Un échange est envisagé pour aligner les angles d'analyse avec 
les besoins de l'observatoire.

## Auteur

Dominique Rigault — Analyste de données géospatiales  
[linkedin.com/in/dominique.rigault](https://linkedin.com/in/dominiquerigault) · 
[github.com/dominique-rigault](https://github.com/dominique-rigault)

## Licence

Données et code publiés sous licence ouverte — réutilisation libre avec attribution.
