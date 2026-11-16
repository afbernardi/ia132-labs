# Module hérité : calcule le total, la livraison et la priorité des commandes.
# Écrit en 2017, « ça marche, on n'y touche pas ». Jusqu'à aujourd'hui.


def traiter(commandes, region, client_premium):
    resultat = []
    for commande in commandes:
        if commande["statut"] != "annulee":
            if commande["poids"] > 0:
                sous_total = 0
                for ligne in commande["lignes"]:
                    sous_total = sous_total + ligne["prix"] * ligne["qte"]
                if region == "QC":
                    if commande["poids"] <= 2:
                        frais_livraison = 8
                    else:
                        if commande["poids"] <= 10:
                            frais_livraison = 15
                        else:
                            frais_livraison = 15 + (commande["poids"] - 10) * 1.5
                elif region == "ON":
                    if commande["poids"] <= 2:
                        frais_livraison = 10
                    else:
                        if commande["poids"] <= 10:
                            frais_livraison = 18
                        else:
                            frais_livraison = 18 + (commande["poids"] - 10) * 1.75
                else:
                    if commande["poids"] <= 2:
                        frais_livraison = 14
                    else:
                        if commande["poids"] <= 10:
                            frais_livraison = 25
                        else:
                            frais_livraison = 25 + (commande["poids"] - 10) * 2.5
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
