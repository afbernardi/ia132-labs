"""Lab 05 — Analyse d'une liste de diffusion.

Correct, testé… et beaucoup trop lent sur les 200 000 abonnés de la vraie liste.
"""


def normaliser(courriel: str) -> str:
    return courriel.strip().lower()


def dedoublonner(courriels: list[str]) -> list[str]:
    """Courriels uniques, normalisés, dans l'ordre de leur PREMIÈRE apparition."""
    resultat = []
    vus = set()
    for c in courriels:
        c = normaliser(c)
        if c not in vus:
            vus.add(c)
            resultat.append(c)
    return resultat


def top_domaines(courriels: list[str], n: int = 3) -> list[tuple[str, int]]:
    """Les n domaines les plus fréquents : (domaine, nombre), par nombre décroissant puis par nom."""
    comptes = {}
    for c in courriels:
        domaine = normaliser(c).split("@")[1]
        comptes[domaine] = comptes.get(domaine, 0) + 1
    tries = sorted(comptes.items(), key=lambda x: (-x[1], x[0]))
    return tries[:n]


def communs(liste_a: list[str], liste_b: list[str]) -> list[str]:
    """Courriels présents dans les deux listes, sans doublon, dans l'ordre de liste_a."""
    b = {normaliser(c) for c in liste_b}
    vus = set()
    resultat = []
    for c in liste_a:
        c = normaliser(c)
        if c not in vus:
            vus.add(c)
            if c in b:
                resultat.append(c)
    return resultat
