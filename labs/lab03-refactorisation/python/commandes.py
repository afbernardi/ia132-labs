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


def traiter(commandes, region, client_premium):
    resultat = []
    for commande in commandes:
        if commande["statut"] != "annulee":
            if commande["poids"] > 0:
                sous_total = 0
                for ligne in commande["lignes"]:
                    sous_total = sous_total + ligne["prix"] * ligne["qte"]
                frais_livraison = _calculer_frais_livraison(commande["poids"], region)
                if client_premium:
                    if sous_total > 100:
                        frais_livraison = 0
                    else:
                        frais_livraison = frais_livraison / 2
                if sous_total > 500:
                    priorite = "haute"
                elif sous_total > 100:
                    priorite = "normale"
                else:
                    priorite = "basse"
                resultat.append({"id": commande["id"], "total": round(sous_total + frais_livraison, 2), "livraison": round(frais_livraison, 2), "priorite": priorite})
            else:
                print("poids invalide " + str(commande["id"]))
    return resultat
