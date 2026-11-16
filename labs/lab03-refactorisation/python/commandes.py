# Module hérité : calcule le total, la livraison et la priorité des commandes.
# Écrit en 2017, « ça marche, on n'y touche pas ». Jusqu'à aujourd'hui.


def _calculer_frais_livraison(poids: int | float, region: str) -> int | float:
    """Calcule les frais de livraison de base.

    Args:
        poids: Poids de la commande.
        region: Code de la région.

    Returns:
        Frais de livraison avant rabais premium.
    """
    if region == "QC":
        if poids <= 2:
            frais_livraison = 8
        else:
            if poids <= 10:
                frais_livraison = 15
            else:
                frais_livraison = 15 + (poids - 10) * 1.5
    elif region == "ON":
        if poids <= 2:
            frais_livraison = 10
        else:
            if poids <= 10:
                frais_livraison = 18
            else:
                frais_livraison = 18 + (poids - 10) * 1.75
    else:
        if poids <= 2:
            frais_livraison = 14
        else:
            if poids <= 10:
                frais_livraison = 25
            else:
                frais_livraison = 25 + (poids - 10) * 2.5
    return frais_livraison


def _calculer_sous_total(lignes: list[dict[str, int | float]]) -> int | float:
    """Calcule le sous-total des lignes d'une commande.

    Args:
        lignes: Lignes de la commande avec leur prix et leur quantite.

    Returns:
        Somme des prix multiplies par les quantites.
    """
    sous_total = 0
    for ligne in lignes:
        sous_total = sous_total + ligne["prix"] * ligne["qte"]
    return sous_total


def _ajuster_frais_premium(
    frais_livraison: int | float,
    sous_total: int | float,
    client_premium: bool,
) -> int | float:
    """Applique les regles de livraison du client premium.

    Args:
        frais_livraison: Frais de livraison de base.
        sous_total: Sous-total de la commande.
        client_premium: Indique si le client est premium.

    Returns:
        Frais apres application des regles premium.
    """
    if client_premium:
        if sous_total > 100:
            frais_livraison = 0
        else:
            frais_livraison = frais_livraison / 2
    return frais_livraison


def _determiner_priorite(sous_total: int | float) -> str:
    """Determine la priorite selon le sous-total.

    Args:
        sous_total: Sous-total de la commande.

    Returns:
        Niveau de priorite de la commande.
    """
    if sous_total > 500:
        priorite = "haute"
    elif sous_total > 100:
        priorite = "normale"
    else:
        priorite = "basse"
    return priorite


def traiter(commandes, region, client_premium):
    resultat = []
    for commande in commandes:
        if commande["statut"] == "annulee":
            continue
        if not (commande["poids"] > 0):
            print("poids invalide " + str(commande["id"]))
            continue
        sous_total = _calculer_sous_total(commande["lignes"])
        frais_livraison = _calculer_frais_livraison(commande["poids"], region)
        frais_livraison = _ajuster_frais_premium(frais_livraison, sous_total, client_premium)
        priorite = _determiner_priorite(sous_total)
        resultat.append({"id": commande["id"], "total": round(sous_total + frais_livraison, 2), "livraison": round(frais_livraison, 2), "priorite": priorite})
    return resultat
