CONTEXTE
Tu écris en Python 3.10+ dans `python/facture.py`. Respecte les conventions du projet : PEP 8, annotations de type, docstrings Google et noms en français sans accents.

TÂCHE
Implémente `calculer_facture(lignes, code_promo=None)` selon toutes les règles métier de `@SPEC.md` (voir aussi `#file:SPEC.md`). Retourne exactement les champs `sous_total`, `rabais`, `livraison`, `tps`, `tvq` et `total`.

CONTRAINTES
- Représente tous les montants en entiers de cents; n’utilise jamais de nombres à virgule flottante.
- Pour chaque pourcentage, arrondis au cent le plus proche, avec les demis vers le haut; n’utilise pas `round()`.
- N’ajoute aucune dépendance.
- Lève `ValueError` pour une facture vide, un prix négatif, une quantité inférieure à 1 ou un code promo inconnu. Ne masque aucune erreur.
- Respecte l’ordre des calculs et les seuils de rabais et de livraison définis dans `SPEC.md`.

FORMAT
Fournis une seule fonction publique `calculer_facture` et, si nécessaire, des fonctions privées. Ne modifie pas les tests.

EXEMPLES
1. Entrée : `lignes=[{"produit": "Article", "prix": 10000, "quantite": 1}]`, `code_promo="ETE15"`
   Résultat : `{"sous_total": 10000, "rabais": 1500, "livraison": 0, "tps": 425, "tvq": 848, "total": 9773}`
2. Entrée : `lignes=[{"produit": "Article", "prix": 7000, "quantite": 1}]`, `code_promo="BIENVENUE10"`
   Résultat : `{"sous_total": 7000, "rabais": 700, "livraison": 999, "tps": 365, "tvq": 729, "total": 8393}`