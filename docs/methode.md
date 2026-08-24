# Méthode d'analyse de l'accessibilité aux réseaux structurants

## Objet de ce document

Ce document décrit la méthode utilisée pour évaluer l'accessibilité d'une
population aux réseaux de transport structurants, et son évolution entre une
situation actuelle et un réseau cible. Il est rédigé pour être compris
indépendamment de son cas d'application, de façon à pouvoir être transposé à
un autre territoire ou à un autre projet de desserte. L'application décrite
ici concerne la Métropole Rouen Normandie (MRN) et le Service Express
Régional Métropolitain (SERM), qui servent d'illustration tout au long du
document.

## Question traitée

> Pour chaque lieu d'habitation, quel est le meilleur niveau de desserte en
> transport en commun structurant atteignable en moins de 15 minutes à pied
> ou à vélo, et quelle part de la population voit ce niveau s'élever avec un
> réseau cible ?

Cette question suppose deux conditions de départ : un réseau de transport
hiérarchisé (tous les arrêts ne se valent pas) et deux états à comparer
(situation actuelle, réseau cible ou projeté).

## Construction de l'indicateur

**Pourquoi ne pas mesurer l'accès à un arrêt quelconque.** Dans un territoire
déjà bien maillé en transport en commun, l'accès binaire à *un* arrêt, de
n'importe quel niveau, est en général saturé : presque tous les habitants en
sont déjà proches. Un tel indicateur ne renseigne pas sur l'apport d'un
projet qui vise le réseau structurant (métro, train, car express) plutôt que
le maillage de proximité. Sur la MRN par exemple, cet indicateur naïf aurait
été incapable de distinguer l'effet du SERM.

**Indicateur retenu.** Le meilleur niveau de desserte structurante
atteignable à pied ou à vélo, les niveaux étant ordonnés par portée
croissante (exemple MRN : aucun < bus < TEOR < métro < car express < train).
La comparaison avant / après compte les habitants dont ce niveau s'élève avec
le réseau cible. Les temps de parcours sont restitués en gradient (par
exemple 5 / 10 / 15 min) plutôt qu'à un seuil unique, pour ne pas masquer les
situations proches du seuil.

**Choix à faire pour transposer l'indicateur à un autre territoire** : établir
la hiérarchie des modes structurants localement pertinents, exclure les modes
marginaux en population ou strictement locaux, et fixer le budget-temps et le
gradient de restitution.

## Deux périmètres à distinguer

- **Offre** (réseau viaire et arrêts) : étendue au-delà du territoire
  d'étude stricte, avec une marge correspondant au budget-temps retenu (dans
  le cas MRN : +3,75 km pour les arrêts, soit 15 min à vélo, +5 km pour le
  réseau viaire), afin de capter les arrêts extérieurs au territoire mais
  plus proches d'un habitant qu'un arrêt interne.
- **Demande** (population) : circonscrite au territoire d'étude strict.

Confondre les deux périmètres sous-estime systématiquement l'accessibilité
des habitants situés en bordure du territoire.

## Données mobilisées

| Donnée | Rôle | Exemple MRN |
|---|---|---|
| Population localisée | Poids démographique de chaque zone | INSEE Filosofi, carroyage 200 m |
| Réseau viaire piéton et cyclable | Support de routage réel | OpenStreetMap (OSMnx) |
| Réseau de transport structurant, situation actuelle | Arrêts et niveaux de desserte existants | GTFS ATOUMOD ([transport.data.gouv.fr](https://transport.data.gouv.fr)) |
| Réseau de transport structurant, situation cible | Arrêts et niveaux de desserte projetés | Documents techniques publics du projet (délibérations, schémas de préfiguration) |
| Armature territoriale | Typologie des lieux desservis (centralités, etc.), utile à la restitution mais non à l'indicateur lui-même | Enrichissement manuel d'un référentiel de communes |

Les trois premières lignes sont couramment disponibles pour un territoire
français. La quatrième dépend du projet étudié : à défaut de couche
SIG officielle pour un réseau cible non encore mis en service, une
géolocalisation manuelle depuis les documents techniques publics est une
solution de repli acceptée, à condition d'en documenter la source précise et
la date.

## Chaîne de traitement

1. **Référentiels transversaux** : périmètre administratif du territoire
   d'étude.
2. **Réseau viaire** : graphes piéton et cyclable en routage réel sur le
   périmètre offre.
3. **Arrêts** : constitution des couches de situation actuelle et de
   situation cible, avec attribut de niveau de desserte, sur le périmètre
   offre.
4. **Isochrones et atteignabilité** : routage réel depuis chaque arrêt,
   traitement paramétré par situation (actuelle, cible), produisant pour
   chaque nœud du réseau le meilleur niveau atteignable et le temps d'accès
   associé.
5. **Population localisée** : couche de population sur le périmètre demande.
6. **Rattachement population/réseau** : chaque zone de population est
   rattachée au réseau pour lire le meilleur niveau atteignable, avec
   correction du tronçon d'approche (cf. note de limites).
7. **Comparaison avant / après** : à l'échelle globale et à un niveau de
   restitution intermédiaire pertinent (commune, quartier, type de
   centralité selon le territoire).

## Application à la Métropole Rouen Normandie

Sur la base de la population Filosofi (453 000 habitants), 30,3 % de la
population gagne au moins un niveau de desserte structurante à pied grâce au
réseau cible SERM, 32,3 % à vélo. Ces résultats sont mobilisables pour trois
décisions : où concentrer le rabattement vers les futures haltes (bus, modes
actifs, stationnement vélo), quels secteurs resteront mal desservis malgré le
réseau cible, et comment objectiver l'équité territoriale d'accès au réseau
structurant.

## Note de limites et domaine de validité

**Ce que la méthode couvre.** L'accessibilité par les modes actifs (marche,
vélo) au réseau structurant, comparée entre deux états d'un même réseau, à
l'échelle d'un territoire disposant d'un réseau viaire cartographié dans
OpenStreetMap et d'une source de population carroyée ou géolocalisée.

**Ce qu'elle ne couvre pas.** Le rabattement en voiture, le confort ou la
sécurité perçue du trajet, l'intermodalité (correspondances), et tout mode de
transport dont la fréquence est trop irrégulière pour être compatible avec
une hypothèse de déplacement continu (à Rouen, les liaisons par bac sur la
Seine ont été exclues pour cette raison, avec une sous-estimation résiduelle
de l'accessibilité des secteurs riverains concernés).

**Précision de localisation de la population.** Un carroyage introduit une
erreur de localisation correspondant à la moitié de la diagonale de la
maille (pour un carroyage de 200 m, jusqu'à 100 m, soit jusqu'à 1,2 min à
pied). Une source de population localisée au bâtiment réduirait cette marge.

**Écart entre sources de population.** Une source de population fiscale ou
d'enquête peut différer de quelques points de pourcentage d'une source de
recensement municipal, du fait de champs de population différents (par
exemple, exclusion des communautés) et d'hypothèses de densité uniforme sur
les zones de bordure du territoire.

**Rattachement au réseau.** Le rattachement d'un arrêt ou d'une zone de
population au nœud ou à l'arête la plus proche du graphe introduit un biais
de l'ordre de quelques dizaines de mètres, comparable à la précision de la
source de population, sauf en secteur d'habitat très dispersé où le graphe
viaire peut comporter des arêtes longues et peu subdivisées. Sur la MRN, ce
cas ne concerne que des arrêts isolés hors hiérarchie structurante, sans
incidence sur l'indicateur retenu.

**Réseau cible non figé.** Lorsque le réseau cible dépend d'un projet en
préfiguration, son phasage opérationnel peut ne pas être arrêté au moment de
l'analyse. La méthode retient alors le réseau cible complet comme terme de
comparaison, indépendamment de son calendrier de déploiement : elle mesure
l'effet du réseau à terme, pas un état daté.

**Dépendance à des référentiels externes vivants.** Le périmètre
administratif et le réseau viaire sont dérivés de bases collaboratives
(OpenStreetMap, GTFS ATOUMOD Normandie) interrogées au moment de l'exécution de la chaîne. Rejouer
l'analyse à une date différente peut donc produire des résultats légèrement
différents si ces bases ont été modifiées entretemps, sans qu'aucune erreur
ne soit signalée. Pour un livrable figé (rapport, restitution officielle), il
est recommandé de conserver une copie horodatée des données sources utilisées.

## Conditions de transposition à un autre territoire

- Disposer d'un réseau viaire piéton et cyclable cartographié (OpenStreetMap
  ou équivalent) et d'un référentiel de transport structurant en situation
  actuelle (GTFS ou équivalent).
- Établir la hiérarchie des modes structurants pertinents localement, et le
  budget-temps de référence (15 min n'est pas une contrainte de la méthode,
  mais un choix à documenter pour chaque territoire).
- Pour un réseau cible non encore en service, prévoir une source de
  géolocalisation manuelle si aucune couche SIG officielle n'existe, et
  documenter sa date et sa provenance.
- Choisir une source de population localisée dont la résolution est cohérente
  avec le budget-temps retenu (un carroyage grossier dégrade la précision
  d'un budget-temps court).
