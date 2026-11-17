"""Utilitaires géographiques pour mesurer des distances entre points et les filtrer.

Le module s'appuie sur la formule haversine pour calculer la distance entre deux
coordonnées géographiques sur une sphère approximative, avec un rayon moyen de la Terre
fixé à 6 371 km. Il est principalement pensé pour comparer des villes et trouver les
points les plus proches d'un emplacement donné.

Exemples:
    >>> from geo import Point, distance_km, dans_le_rayon, plus_proche, format_coordonnees
    >>> MTL = Point("Montréal", 45.5019, -73.5674)
    >>> QC = Point("Québec", 46.8139, -71.2080)
    >>> distance_km(MTL, QC)
    233.0
    >>> [p.nom for p in dans_le_rayon(MTL, [QC], 250)]
    ['Québec']
"""

from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt

RAYON_TERRE_KM = 6371.0


@dataclass(frozen=True)
class Point:
    """Représente un point géographique identifié par son nom et ses coordonnées.

    Attributes:
        nom: Nom lisible du point, par exemple le nom d'une ville.
        lat: Latitude en degrés, positive dans l'hémisphère nord.
        lon: Longitude en degrés, positive à l'est du méridien de Greenwich.

    Example:
        >>> Point("Montréal", 45.5019, -73.5674)
        Point(nom='Montréal', lat=45.5019, lon=-73.5674)
    """

    nom: str
    lat: float
    lon: float


def distance_km(a: Point, b: Point) -> float:
    """Calcule la distance en kilomètres entre deux points géographiques.

    La formule de l'haversine prend en compte la courbure de la Terre à l'aide d'une
    approximation sphérique. Le résultat est arrondi à un décimètre pour obtenir une
    distance facilement lisible en tests et en sortie utilisateur.

    Args:
        a: Point de départ.
        b: Point d'arrivée.

    Returns:
        La distance en kilomètres entre ``a`` et ``b``, arrondie à 0,1 km près.

    Example:
        >>> MTL = Point("Montréal", 45.5019, -73.5674)
        >>> QC = Point("Québec", 46.8139, -71.2080)
        >>> distance_km(MTL, QC)
        233.0
    """
    dlat = radians(b.lat - a.lat)
    dlon = radians(b.lon - a.lon)
    h = sin(dlat / 2) ** 2 + cos(radians(a.lat)) * cos(radians(b.lat)) * sin(dlon / 2) ** 2
    return round(2 * RAYON_TERRE_KM * asin(sqrt(h)), 1)


def dans_le_rayon(centre: Point, points: list[Point], rayon_km: float) -> list[Point]:
    """Retourne les points à l'intérieur d'un rayon donné autour d'un centre.

    Les points sont triés selon leur distance au centre, du plus proche au plus loin.
    L'intervalle est inclus : un point situé exactement à la limite du rayon est conservé.

    Args:
        centre: Point central à partir duquel la distance est calculée.
        points: Liste de points à évaluer.
        rayon_km: Distance maximale autorisée en kilomètres.

    Returns:
        Une liste de points situés à ``rayon_km`` ou moins du centre, classée par distance
        croissante.

    Raises:
        ValueError: Si ``rayon_km`` est strictement négatif.

    Example:
        >>> MTL = Point("Montréal", 45.5019, -73.5674)
        >>> QC = Point("Québec", 46.8139, -71.2080)
        >>> OTT = Point("Ottawa", 45.4215, -75.6972)
        >>> TR = Point("Trois-Rivières", 46.3430, -72.5477)
        >>> SH = Point("Sherbrooke", 45.4042, -71.8929)
        >>> [p.nom for p in dans_le_rayon(MTL, [QC, OTT, TR, SH], 150)]
        ['Trois-Rivières', 'Sherbrooke']
        >>> dans_le_rayon(MTL, [QC], -1)
        Traceback (most recent call last):
        ...
        ValueError: rayon négatif
    """
    if rayon_km < 0:
        raise ValueError("rayon négatif")
    return sorted((p for p in points if distance_km(centre, p) <= rayon_km), key=lambda p: distance_km(centre, p))


def plus_proche(origine: Point, points: list[Point]) -> Point | None:
    """Trouve le point le plus proche de l'origine sans le considérer comme candidat.

    Le point d'origine est exclu de la recherche afin d'éviter de retourner le même point
    lorsque la liste inclut déjà la position de départ.

    Args:
        origine: Point de référence.
        points: Liste des points parmi lesquels chercher.

    Returns:
        Le point le plus proche de ``origine`` ; ``None`` si la liste ne contient qu'un seul
        élément ou si elle est vide.

    Example:
        >>> MTL = Point("Montréal", 45.5019, -73.5674)
        >>> QC = Point("Québec", 46.8139, -71.2080)
        >>> OTT = Point("Ottawa", 45.4215, -75.6972)
        >>> TR = Point("Trois-Rivières", 46.3430, -72.5477)
        >>> SH = Point("Sherbrooke", 45.4042, -71.8929)
        >>> plus_proche(MTL, [MTL, QC, OTT, TR, SH]) == TR
        True
        >>> plus_proche(MTL, [MTL]) is None
        True
    """
    candidats = [p for p in points if p != origine]
    return min(candidats, key=lambda p: distance_km(origine, p), default=None)


def format_coordonnees(p: Point) -> str:
    """Formate une latitude et une longitude en notation de degrés cardinales.

    Le résultat est présenté sous la forme ``DDDD.DDDD° N/S, DDDDD.DDDD° E/O`` avec des
    coordonnées absolues arrondies à 4 décimales.

    Args:
        p: Point géographique à formater.

    Returns:
        Une chaîne lisible comme ``45.5019° N, 73.5674° O``.

    Example:
        >>> format_coordonnees(Point("Montréal", 45.5019, -73.5674))
        '45.5019° N, 73.5674° O'
    """
    ns = "N" if p.lat >= 0 else "S"
    eo = "E" if p.lon >= 0 else "O"
    return f"{abs(p.lat):.4f}° {ns}, {abs(p.lon):.4f}° {eo}"
