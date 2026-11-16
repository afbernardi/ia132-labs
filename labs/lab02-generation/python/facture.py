"""Lab 02 — Calcul d'une facture avec TPS et TVQ.

À générer avec votre assistant à partir de SPEC.md (voir README).
Tous les montants sont des entiers, en cents.
"""


def calculer_facture(lignes: list[dict], code_promo: str | None = None) -> dict[str, int]:
    """Calcule une facture à partir de lignes {"produit", "prix", "quantite"}.

    Retourne {"sous_total", "rabais", "livraison", "tps", "tvq", "total"}, en cents.
    Les règles complètes sont dans SPEC.md.
    """
    if not lignes:
        raise ValueError("Facture vide")

    sous_total = 0
    for ligne in lignes:
        prix = ligne["prix"]
        quantite = ligne["quantite"]
        if type(prix) is not int or prix < 0:
            raise ValueError("Le prix doit être un entier positif ou nul")
        if type(quantite) is not int or quantite < 1:
            raise ValueError("La quantité doit être un entier supérieur ou égal à 1")
        sous_total += prix * quantite

    code_normalise = code_promo.strip().upper() if code_promo is not None else ""
    if code_normalise == "BIENVENUE10":
        rabais = _arrondir_pourcentage(sous_total, 10, 100)
    elif code_normalise == "ETE15":
        rabais = (
            _arrondir_pourcentage(sous_total, 15, 100)
            if sous_total >= 10_000
            else 0
        )
    elif code_normalise == "":
        rabais = 0
    else:
        raise ValueError("Code promo inconnu")

    livraison = 0 if sous_total - rabais >= 7_500 else 999
    base_taxable = sous_total - rabais + livraison
    tps = _arrondir_pourcentage(base_taxable, 5, 100)
    tvq = _arrondir_pourcentage(base_taxable, 399, 4_000)
    total = base_taxable + tps + tvq

    return {
        "sous_total": sous_total,
        "rabais": rabais,
        "livraison": livraison,
        "tps": tps,
        "tvq": tvq,
        "total": total,
    }


def _arrondir_pourcentage(montant: int, numerateur: int, denominateur: int) -> int:
    """Calcule un pourcentage positif en arrondissant les demis vers le haut."""
    return (2 * montant * numerateur + denominateur) // (2 * denominateur)
