"""Persistance JSON des tâches."""

import json
from pathlib import Path

from taches.modele import Tache, convertir_echeance


class Depot:
    """Charge et enregistre les tâches dans un fichier JSON."""

    def __init__(self, fichier: Path):
        """Initialise le dépôt.

        Args:
            fichier: Chemin du fichier JSON à utiliser.
        """
        self.fichier = fichier

    def charger(self) -> tuple[list[Tache], int]:
        """Charge les tâches et le prochain identifiant.

        Returns:
            La liste des tâches et le prochain identifiant à attribuer.

        Raises:
            ValueError: Si le contenu JSON ne respecte pas le format du dépôt.
        """
        if not self.fichier.exists():
            return [], 1

        donnees = json.loads(self.fichier.read_text(encoding="utf-8"))
        if not isinstance(donnees, dict):
            raise ValueError("Le fichier de tâches doit contenir un objet JSON.")

        prochain_id = donnees.get("prochain_id")
        donnees_taches = donnees.get("taches")
        if isinstance(prochain_id, bool) or not isinstance(prochain_id, int) or prochain_id < 1:
            raise ValueError("Le prochain identifiant du dépôt est invalide.")
        if not isinstance(donnees_taches, list):
            raise ValueError("La liste des tâches du dépôt est invalide.")

        taches = [self._creer_tache(donnees_tache, index) for index, donnees_tache in enumerate(donnees_taches)]
        identifiants = [tache.id for tache in taches]
        if len(set(identifiants)) != len(identifiants):
            raise ValueError("Le fichier contient des identifiants de tâche en double.")
        if any(identifiant >= prochain_id for identifiant in identifiants):
            raise ValueError("Le prochain identifiant doit être supérieur à tous les identifiants existants.")
        return taches, prochain_id

    def enregistrer(self, taches: list[Tache], prochain_id: int) -> None:
        """Enregistre les tâches et le prochain identifiant.

        Args:
            taches: Tâches à persister.
            prochain_id: Identifiant qui sera attribué à la prochaine tâche.

        Raises:
            ValueError: Si le prochain identifiant n'est pas valide.
        """
        if isinstance(prochain_id, bool) or not isinstance(prochain_id, int) or prochain_id < 1:
            raise ValueError("Le prochain identifiant du dépôt est invalide.")
        identifiants = [tache.id for tache in taches]
        if len(set(identifiants)) != len(identifiants):
            raise ValueError("Le dépôt ne peut pas enregistrer des identifiants en double.")
        if any(identifiant >= prochain_id for identifiant in identifiants):
            raise ValueError("Le prochain identifiant doit être supérieur à tous les identifiants existants.")

        donnees = {
            "prochain_id": prochain_id,
            "taches": [self._serialiser_tache(tache) for tache in taches],
        }
        contenu = json.dumps(donnees, ensure_ascii=False, indent=2) + "\n"
        self.fichier.write_text(contenu, encoding="utf-8")

    @staticmethod
    def _creer_tache(donnees: object, index: int) -> Tache:
        """Reconstruit une tâche depuis une entrée JSON."""
        if not isinstance(donnees, dict):
            raise ValueError(f"La tâche à la position {index} doit être un objet JSON.")
        try:
            return Tache(
                id=donnees["id"],
                titre=donnees["titre"],
                priorite=donnees["priorite"],
                echeance=convertir_echeance(donnees["echeance"]),
                etiquettes=donnees["etiquettes"],
                terminee=donnees["terminee"],
            )
        except (KeyError, TypeError, ValueError) as erreur:
            raise ValueError(f"La tâche à la position {index} est invalide.") from erreur

    @staticmethod
    def _serialiser_tache(tache: Tache) -> dict[str, object]:
        """Convertit une tâche en objet compatible avec le fichier JSON."""
        return {
            "id": tache.id,
            "titre": tache.titre,
            "priorite": tache.priorite,
            "echeance": tache.echeance.isoformat() if tache.echeance is not None else None,
            "etiquettes": tache.etiquettes,
            "terminee": tache.terminee,
        }
