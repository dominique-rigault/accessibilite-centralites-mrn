# Politique de sécurité

## Périmètre

Ce dépôt analyse les données de mobilité de la Métropole Rouen Normandie :
transports en commun (GTFS ATOUMOD), vélos en libre-service (Lovélo), réseau
ferroviaire. Les données proviennent d'API publiques et de jeux open data.

Sont considérées comme vulnérabilités pertinentes :

- Secrets exposés : clés API (SNCF, GBFS…), tokens d'authentification,
  identifiants de connexion présents dans le code, les notebooks ou l'historique Git.
- Dépendances Python présentant une CVE connue.
- Failles dans les cartes interactives exportées en HTML (XSS, injection).
- Données personnelles accidentellement incluses (coordonnées d'usagers, traces
  de déplacements individuels).

## Signaler une vulnérabilité

Merci de **ne pas ouvrir d'issue publique** pour les signalements de sécurité.

Contactez-moi par email : **dominique.rigault@outlook.com**

Indiquez si possible :

- La nature du problème.
- Le fichier ou le commit concerné.
- Les étapes pour reproduire le problème.

Je m'engage à accuser réception sous 7 jours et à traiter le signalement
dans un délai raisonnable.

## Divulgation

Une fois le problème corrigé, un résumé pourra être publié dans les notes de version
du dépôt. Les contributeurs qui signalent des vulnérabilités seront crédités
(sauf demande contraire).
