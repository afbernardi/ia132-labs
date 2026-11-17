# Changelog

Les changements notables du lab 06 sont consignés dans ce fichier.

## [Unreleased]

### Ajouté
- Documentation du module géographique, de la classe `Point` et de ses fonctions publiques.
- Exemples exécutables avec `doctest` dans les docstrings.
- README du module Python présentant son but, son installation, un exemple d'utilisation et ses limites.

### Modifié
- Docstrings harmonisées au format Google, avec les sections `Args:`, `Returns:` et `Raises:` selon le comportement documenté.
- Explications précisées sur le calcul de distance par la formule de l'haversine, le tri par proximité et l'inclusion de la limite du rayon.

### Corrigé
- Exemples de documentation vérifiés pour correspondre au comportement réel du code.
- Descriptions clarifiées pour indiquer que `plus_proche` exclut l'origine et que `dans_le_rayon` lève une `ValueError` pour un rayon négatif.
- Validation des tests de comportement et des exemples documentés du module Python.
