# Module géographique

## But MAJ Arnaldo

Ce module fournit des outils pour manipuler des points géographiques et effectuer des calculs de proximité. Il permet de :

- calculer la distance en kilomètres entre deux points ;
- filtrer les points situés dans un rayon donné autour d'un centre ;
- retrouver le point le plus proche d'une position donnée ;
- formater des coordonnées en notation lisible.

Le calcul repose sur la formule de l'haversine, une approximation de la distance sur une sphère terrestre.

## Installation

Aucune dépendance externe n'est nécessaire. Le module fonctionne avec Python 3.10 ou version ultérieure.

```bash
cd labs/lab06-documentation/python
python -m pytest test_geo.py
```

## Exemple d'utilisation

```python
from geo import Point, distance_km, dans_le_rayon, plus_proche, format_coordonnees

mtl = Point("Montréal", 45.5019, -73.5674)
qc = Point("Québec", 46.8139, -71.2080)
ott = Point("Ottawa", 45.4215, -75.6972)

print(distance_km(mtl, qc))
# 233.0

print([p.nom for p in dans_le_rayon(mtl, [qc, ott], 200)])
# ['Québec']

print(plus_proche(mtl, [mtl, qc, ott]).nom)
# Québec

print(format_coordonnees(mtl))
# 45.5019° N, 73.5674° O
```

## Limites

- La distance est calculée selon une approximation sphérique de la Terre, donc elle n'est pas exacte à des fins de cartographie de précision.
- Le module suppose des coordonnées en degrés décimaux standard et ne gère pas les projections cartographiques.
- Les valeurs sont arrondies à 0,1 km, ce qui convient pour l'affichage et les tests, mais pas pour une précision métrique fine.
- La validation des entrées est minimale : les objets doivent être des `Point` valides pour obtenir des résultats fiables.
- Le module ne prend pas en charge l'altitude ni les corrections géodésiques plus avancées.

## Vérification

Le comportement est vérifié par les tests dans [test_geo.py](./test_geo.py), et les exemples de documentation sont validés par `doctest`.
