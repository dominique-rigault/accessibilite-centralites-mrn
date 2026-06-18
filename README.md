# Accessibilité bas carbone aux centralités
## Métropole Rouen Normandie — Impact du SERM 2030

Analyse de l'accessibilité piétonne et cyclable aux réseaux de transports 
en commun structurants, avant et après la mise en service du Service Express 
Régional Métropolitain (SERM) à l'horizon 2030.

## Question analytique

> Pour chaque lieu d'habitation, quel est le meilleur niveau de desserte 
> en transport en commun structurant atteignable en moins de 15 minutes 
> à pied ou à vélo, et quelle part de la population voit ce niveau s'élever 
> avec le SERM 2030 ?

**Indicateur retenu.** L'accès binaire à un arrêt *quelconque* est saturé à
l'échelle de l'agglomération (presque tout habitant est à moins de 15 min d'un
arrêt) : il ne mesure pas ce que change le SERM, qui agit sur le réseau
structurant et non sur le maillage bus. L'indicateur est donc le **meilleur
niveau de desserte structurante atteignable** à pied ou à vélo, ordonné par
portée croissante :

`aucun < bus < TEOR < métro < car express < train (SERM)`

La lecture avant / après mesure le nombre d'habitants dont ce niveau s'élève
avec le SERM 2030. Les temps de parcours sont restitués en gradient
(5 / 10 / 15 min) plutôt qu'à un seuil unique. Le bac, structurant sur son seul
corridor et marginal en population, est exclu de la hiérarchie.

**Périmètres d'analyse.** Deux périmètres sont distingués : l'*offre* (réseaux
viaires + arrêts) est étendue à la MRN augmentée d'un tampon +3 750 m pour les
arrêts (15 min à vélo), +5 000 m pour les graphes viaires, afin de capter les
arrêts hors MRN plus proches d'un habitant qu'un arrêt interne; la *demande*
(population Filosofi) reste circonscrite à la MRN stricte.

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
- Population et logements : INSEE Filosofi carroyé 200 m
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
| `01_acquisition_donnees_OSM.ipynb` | Réseaux viaires piéton et cyclable (OSMnx), périmètre offre (MRN + tampon 5 km) | `data/reseau_{pieton,velo}_MRN.gpkg` + `.graphml` |
| `02_arrets_TC.ipynb` | Couche d'arrêts TC 2026 depuis le GTFS ATOUMOD, périmètre offre (MRN + tampon 3,75 km), attribut de niveau de desserte | `data/arrets_2026.gpkg` |
| `03_isochrones.ipynb` | Isochrones piétonnes et cyclables en routage réel depuis les arrêts (niveau de desserte conservé), et table du meilleur niveau atteignable par nœud x niveau du réseau | `data/isochrones_2026.gpkg` + `data/acces_noeuds_2026.gpkg`|
| `04_logements.ipynb` | Couche de population localisée (Filosofi 200 m, découpe MRN stricte) | `data/population_carreaux_MRN.gpkg` |
| `05_logements_accessibilite.ipynb` *— à venir* | Rattachement des carreaux de population au réseau (snap-to-edge) et lecture du meilleur niveau de desserte atteignable par carreau | `data/population_accessibilite_MRN.gpkg` |
| `06_comparaison_avant_apres.ipynb` *— à venir* | Vue différentielle 2026 / SERM 2030 : habitants gagnant un niveau de desserte | — |

> Chaque notebook documente en tête ses prérequis, entrées et sorties détaillés.

## Restitution & aide à la décision

Au-delà des cartes d'isochrones, l'analyse est construite pour produire une
lecture directement actionnable :

- **Part de population atteignant une desserte structurante (< 15 min), et
  niveau atteint, avant / après SERM** à l'échelle métropolitaine, puis par
  commune et par type de centralité : l'indicateur d'équité territoriale.
- **Secteurs habités en déficit d'accès malgré le SERM 2030** cartographie des
  zones où se posent les arbitrages de rabattement et d'aménagement.
- **Gain marginal du SERM** nombre d'habitants qui gagnent au moins un niveau
  de desserte grâce aux nouvelles haltes, pour objectiver l'apport du projet.

Forme de la recommandation visée : *« prioriser [tel aménagement] sur [tel
secteur], qui ramène le plus d'habitants aujourd'hui mal desservis sous le seuil
d'accessibilité, au meilleur rapport coût / population atteinte. »*

*(Indicateurs chiffrés à compléter à l'issue des notebooks `03`, `05` et `06`.)*

## Limites et données manquantes

- **Écart de population** : population fiscale Filosofi 2021 (453 k individus de ménages) inférieure d'environ 8 % à la population municipale 2021 (491 k), différence imputable au champ des ménages fiscaux (hors population des communautés) et dans une moindre mesure aux carreaux imputés et à l'hypothèse de densité uniforme pour les carreaux traversés par la limite de la MRN.
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
- **Rattachement des arrêts au réseau (snap-to-node)** : chaque arrêt est routé
  depuis le nœud du graphe le plus proche, le tronçon d'approche n'étant ni routé
  ni décompté du budget-temps. Pour les modes structurants (Métro, TEOR, Train),
  qui portent l'indicateur, ce rattachement reste sous 70 m dans tous les cas
  (médiane 15 m à pied, 23 m à vélo ; p95 ≤ 50 m), soit moins d'une minute de
  parcours — du même ordre que l'imprécision du carroyage. Le maillage bus,
  hors hiérarchie, présente un arrêt isolé à 460 m, sans incidence sur l'analyse.
  - **Arrêts sur arêtes longues (zones à habitat dispersé)** : le rattachement au
  nœud le plus proche (et non à l'arête) atteint sa limite lorsqu'un arrêt se
  situe au milieu d'une arête OSM longue et non subdivisée, fréquente en secteur
  rural. L'arrêt est alors routé depuis une extrémité de l'arête : un arrêt de
  desserte rurale (Le Conihout, Le Mesnil-sous-Jumièges, ligne de bus 206) est
  ainsi rattaché à 460 m alors que le réseau passe sous l'arrêt. Le cas ne
  concerne que des arrêts bus isolés en zone peu peuplée, hors hiérarchie
  structurante : aucune incidence sur l'indicateur. Un *snap-to-edge* (insertion
  d'un nœud temporaire sur l'arête) corrigerait ce biais résiduel — réservé à une
  phase ultérieure si un routage fin du réseau bus rural devenait nécessaire.

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

Dominique Rigault, analyste de données géospatiales  
[linkedin.com/in/dominiquerigault](https://linkedin.com/in/dominiquerigault) · 
[github.com/dominique-rigault](https://github.com/dominique-rigault)

## Licence

Données et code publiés sous licence ouverte, réutilisation libre avec attribution.
