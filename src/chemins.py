"""Chemins du projet, indépendants du répertoire d'exécution.

Chaque notebook du dossier `notebooks/` peut être ouvert et exécuté depuis
n'importe quel répertoire de travail (Jupyter, VS Code, ligne de commande).
Ce module fixe la racine du projet à partir de l'emplacement du fichier
lui-même (`src/chemins.py` est toujours à un niveau sous la racine) et non du
répertoire courant, ce qui rend son usage identique quel que soit le contexte
d'exécution.

Prérequis : le projet doit être installé en mode éditable (`pip install -e .`)
pour que `import src.chemins` fonctionne depuis un notebook. Voir le README,
section « Installation et exécution ».
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = ROOT / "notebooks"
DOCS_DIR = ROOT / "docs"
DATA_DIR = ROOT / "data"
RAW_DIR = ROOT / "raw"
CACHE_DIR = ROOT / "cache"
