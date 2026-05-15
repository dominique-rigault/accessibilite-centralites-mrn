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

## Stack technique

`Python` `GeoPandas` `OSMnx` `PostGIS` `Folium` `QGIS` `Jupyter`

## Sources de données

- Réseaux viaires piétons et cyclables : OpenStreetMap (OSMnx)
- Réseaux TC : transport.data.gouv.fr
- Population et logements : INSEE FiLoSoFi carroyé 200 m
- Haltes SERM projetées : délibération du Conseil métropolitain 15/12/2025
- Armature urbaine :
    Fichier des 71 communes de la MRN avec leur type de centralité.
    **Sources** :
    Liste des communes : [COG data.gouv.fr](https://www.data.gouv.fr/datasets/code-officiel-geographique-cog)
    Types de centralité : PAS Métropole Rouen Normandie 2050, carte n°4
    **Méthode** : enrichissement manuel du COG
    Ce fichier ne peut pas être régénéré automatiquement.

## Limites et données manquantes


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
[linkedin.com/in/dominique.rigault](https://linkedin.com/in/dominique.rigault) · 
[github.com/dominique-rigault](https://github.com/dominique-rigault)

## Licence

Données et code publiés sous licence ouverte — réutilisation libre avec attribution.