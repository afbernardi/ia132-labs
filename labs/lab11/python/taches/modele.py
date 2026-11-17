"""Modèle métier des tâches du gestionnaire."""

from dataclasses import dataclass, field
from datetime import date
from typing import Literal

Priorite = Literal["haute", "normale", "basse"]
PRIORITES: tuple[Priorite, ...] = ("haute", "normale", "basse")


@dataclass
class Tache:
    """Représente une tâche et valide ses données métier.

    Attributes:
        id: Identifiant positif de la tâche.
        titre: Titre non vide de la tâche.
        priorite: Priorité de la tâche.
        echeance: Échéance de la tâche, si elle existe.
        etiquettes: Étiquettes associées à la tâche.
        terminee: Indique si la tâche est terminée.
    """

    id: int
    titre: str
    priorite: Priorite = "normale"
    echeance: date | None = None
    etiquettes: list[str] = field(default_factory=list)
    terminee: bool = False

    def __post_init__(self) -> None:
        """Vérifie les invariants de la tâche."""
        if isinstance(self.id, bool) or not isinstance(self.id, int) or self.id < 1:
            raise ValueError("L'identifiant doit être un entier positif.")
        if not isinstance(self.titre, str) or not self.titre.strip():
            raise ValueError("Le titre ne peut pas être vide.")
        if self.priorite not in PRIORITES:
            raise ValueError("La priorité doit être haute, normale ou basse.")
        if self.echeance is not None and type(self.echeance) is not date:
            raise ValueError("L'échéance doit être une date ou None.")
        if not isinstance(self.etiquettes, list) or not all(isinstance(etiquette, str) for etiquette in self.etiquettes):
            raise ValueError("Les étiquettes doivent être une liste de textes.")
        if not isinstance(self.terminee, bool):
            raise ValueError("L'état terminée doit être un booléen.")


def convertir_echeance(valeur: str | None) -> date | None:
    """Convertit une échéance au format strict AAAA-MM-JJ.

    Args:
        valeur: Date à convertir, ou None si la tâche n'a pas d'échéance.

    Returns:
        La date convertie, ou None.

    Raises:
        ValueError: Si la date n'est pas au format AAAA-MM-JJ ou n'existe pas.
    """
    if valeur is None:
        return None
    if not isinstance(valeur, str):
        raise ValueError("L'échéance doit être au format AAAA-MM-JJ.")
    try:
        echeance = date.fromisoformat(valeur)
    except ValueError as erreur:
        raise ValueError(f"Échéance invalide : {valeur!r}. Le format attendu est AAAA-MM-JJ.") from erreur
    if echeance.isoformat() != valeur:
        raise ValueError(f"Échéance invalide : {valeur!r}. Le format attendu est AAAA-MM-JJ.")
    return echeance
