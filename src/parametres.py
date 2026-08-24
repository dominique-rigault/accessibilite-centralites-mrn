"""Paramètres partagés de l'analyse d'accessibilité.

Ces valeurs sont utilisées par plusieurs notebooks (`02`, `03`, `05`); les
centraliser ici évite les divergences silencieuses entre notebooks exécutés
séparément (cf. contrôles de cohérence documentés dans `methode.md`).
"""

# Système de coordonnées du projet
CRS_PROJET = "EPSG:2154"

# Vitesses de déplacement retenues (référence Cerema / INSEE, cf. cadrage)
VITESSE_PIED_KMH = 5
VITESSE_VELO_KMH = 15

# Seuil d'accessibilité et gradient de restitution (minutes)
SEUIL_ACCESSIBILITE_MIN = 15
PAS_TRANCHE_MIN = 5
TRANCHES_MIN = list(range(PAS_TRANCHE_MIN, SEUIL_ACCESSIBILITE_MIN + 1, PAS_TRANCHE_MIN))

# Périmètres offre : tampon autour de la MRN pour ne pas tronquer les
# isochrones des arrêts proches de la limite (cf. cadrage, offre vs demande)
TAMPON_ARRETS_M = 3750   # 15 min à vélo
TAMPON_VIAIRE_M = 5000   # marge de routage, > tampon arrêts

# Lignes TEOR (mode structurant urbain, distinct du bus dans le GTFS ATOUMOD)
TEOR_LINES = {"T1", "T2", "T3", "T4", "T5"}

# Hiérarchie des niveaux de desserte, par portée structurante croissante
# (bac exclu : structurant sur son seul corridor, marginal en population)
NIVEAUX = {"Bus": 1, "TEOR": 2, "Métro": 3, "Car express": 4, "Train": 5}
LIBELLE_NIVEAU = {v: k for k, v in NIVEAUX.items()} | {0: "aucun"}
STRUCTURANTS = ["Train", "Car express", "Métro", "TEOR"]
