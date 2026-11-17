"""Interface en ligne de commande du gestionnaire de tâches."""

import csv
import io
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Literal

from taches.depot import Depot
from taches.modele import PRIORITES, Priorite, Tache, convertir_echeance

FormatExport = Literal["json", "csv"]


@dataclass(frozen=True)
class _Ajouter:
    titre: str
    priorite: Priorite
    echeance: date | None
    etiquettes: list[str]


@dataclass(frozen=True)
class _Lister:
    toutes: bool
    etiquette: str | None
    priorite: Priorite | None


@dataclass(frozen=True)
class _Terminer:
    identifiant: int


@dataclass(frozen=True)
class _Supprimer:
    identifiant: int


@dataclass(frozen=True)
class _EnRetard:
    aujourdhui: date


@dataclass(frozen=True)
class _Exporter:
    format: FormatExport


@dataclass(frozen=True)
class _Kanban:
    pass


_Commande = _Ajouter | _Lister | _Terminer | _Supprimer | _EnRetard | _Exporter | _Kanban


def main(argv: list[str], fichier: Path) -> tuple[int, str]:
    """Exécute une commande et retourne son code et son texte de sortie.

    Args:
        argv: Arguments de commande, sans le nom du programme.
        fichier: Chemin du fichier JSON des tâches.

    Returns:
        Un couple composé du code de sortie et du texte à afficher.
    """
    try:
        commande = _analyser_commande(argv)
    except ValueError as erreur:
        return 2, f"Erreur : {erreur}"
    return _executer_commande(commande, Depot(fichier))


def _analyser_commande(argv: list[str]) -> _Commande:
    """Valide les arguments et construit la commande correspondante."""
    if not argv:
        raise ValueError("Aucune commande fournie.")
    nom, arguments = argv[0], argv[1:]
    analyseurs = {
        "ajouter": _analyser_ajouter,
        "lister": _analyser_lister,
        "terminer": _analyser_terminer,
        "supprimer": _analyser_supprimer,
        "en-retard": _analyser_en_retard,
        "exporter": _analyser_exporter,
        "dashbord-kanban": _analyser_kanban,
    }
    if nom not in analyseurs:
        raise ValueError(f"Commande inconnue : {nom}")
    return analyseurs[nom](arguments)


def _analyser_ajouter(arguments: list[str]) -> _Ajouter:
    """Valide les arguments de la commande ajouter."""
    if not arguments or not arguments[0].strip():
        raise ValueError("Le titre ne peut pas être vide.")
    titre = arguments[0]
    priorite: Priorite = "normale"
    echeance: date | None = None
    etiquettes: list[str] = []
    priorite_vue = False
    echeance_vue = False
    index = 1
    while index < len(arguments):
        option = arguments[index]
        valeur, index = _lire_valeur(arguments, index, option)
        if option == "--priorite" and not priorite_vue:
            priorite = _convertir_priorite(valeur)
            priorite_vue = True
        elif option == "--echeance" and not echeance_vue:
            echeance = convertir_echeance(valeur)
            echeance_vue = True
        elif option == "--etiquette":
            if not valeur:
                raise ValueError("L'étiquette ne peut pas être vide.")
            etiquettes.append(valeur)
        elif option in ("--priorite", "--echeance"):
            raise ValueError(f"L'option {option} ne peut être utilisée qu'une fois.")
        else:
            raise ValueError(f"Option inconnue : {option}")
    return _Ajouter(titre, priorite, echeance, etiquettes)


def _analyser_lister(arguments: list[str]) -> _Lister:
    """Valide les arguments de la commande lister."""
    toutes = False
    etiquette = None
    priorite = None
    index = 0
    while index < len(arguments):
        option = arguments[index]
        if option == "--toutes" and not toutes:
            toutes = True
            index += 1
        elif option == "--etiquette" and etiquette is None:
            etiquette, index = _lire_valeur(arguments, index, option)
            if not etiquette:
                raise ValueError("L'étiquette ne peut pas être vide.")
        elif option == "--priorite" and priorite is None:
            valeur, index = _lire_valeur(arguments, index, option)
            priorite = _convertir_priorite(valeur)
        else:
            raise ValueError(f"Option inconnue ou répétée : {option}")
    return _Lister(toutes, etiquette, priorite)


def _analyser_terminer(arguments: list[str]) -> _Terminer:
    """Valide les arguments de la commande terminer."""
    return _Terminer(_lire_identifiant(arguments))


def _analyser_supprimer(arguments: list[str]) -> _Supprimer:
    """Valide les arguments de la commande supprimer."""
    return _Supprimer(_lire_identifiant(arguments))


def _analyser_en_retard(arguments: list[str]) -> _EnRetard:
    """Valide les arguments de la commande en-retard."""
    if len(arguments) != 2 or arguments[0] != "--aujourdhui":
        raise ValueError("Usage : en-retard --aujourdhui AAAA-MM-JJ.")
    aujourdhui = convertir_echeance(arguments[1])
    if aujourdhui is None:
        raise ValueError("Une date est requise pour --aujourdhui.")
    return _EnRetard(aujourdhui)


def _analyser_exporter(arguments: list[str]) -> _Exporter:
    """Valide les arguments de la commande exporter."""
    if len(arguments) != 2 or arguments[0] != "--format":
        raise ValueError("Usage : exporter --format json|csv.")
    if arguments[1] not in ("json", "csv"):
        raise ValueError("Le format d'export doit être json ou csv.")
    return _Exporter(arguments[1])


def _analyser_kanban(arguments: list[str]) -> _Kanban:
    """Valide les arguments de la commande dashbord-kanban."""
    if arguments:
        raise ValueError("La commande dashbord-kanban n'accepte aucun argument.")
    return _Kanban()


def _lire_valeur(arguments: list[str], index: int, option: str) -> tuple[str, int]:
    """Retourne la valeur qui suit une option et l'index suivant."""
    if index + 1 >= len(arguments):
        raise ValueError(f"L'option {option} exige une valeur.")
    return arguments[index + 1], index + 2


def _lire_identifiant(arguments: list[str]) -> int:
    """Valide un identifiant positif fourni en argument."""
    if len(arguments) != 1 or not arguments[0].isascii() or not arguments[0].isdecimal():
        raise ValueError("Un identifiant entier positif est requis.")
    identifiant = int(arguments[0])
    if identifiant < 1:
        raise ValueError("Un identifiant entier positif est requis.")
    return identifiant


def _convertir_priorite(valeur: str) -> Priorite:
    """Valide et retourne une priorité."""
    if valeur == "haute":
        return "haute"
    if valeur == "normale":
        return "normale"
    if valeur == "basse":
        return "basse"
    raise ValueError("La priorité doit être haute, normale ou basse.")


def _executer_commande(commande: _Commande, depot: Depot) -> tuple[int, str]:
    """Charge les données et exécute une commande déjà validée."""
    taches, prochain_id = depot.charger()
    if isinstance(commande, _Ajouter):
        return _executer_ajouter(commande, taches, prochain_id, depot)
    if isinstance(commande, _Lister):
        return 0, _formater_liste(taches, commande.toutes, commande.etiquette, commande.priorite)
    if isinstance(commande, (_Terminer, _Supprimer)):
        return _executer_modification(commande, taches, prochain_id, depot)
    if isinstance(commande, _EnRetard):
        return 0, _formater_liste(taches, date_limite=commande.aujourdhui)
    if isinstance(commande, _Exporter):
        return 0, _exporter_taches(taches, commande.format)
    if isinstance(commande, _Kanban):
        return 0, _formater_kanban(taches)
    raise AssertionError("Type de commande non pris en charge.")


def _executer_ajouter(
    commande: _Ajouter, taches: list[Tache], prochain_id: int, depot: Depot
) -> tuple[int, str]:
    """Crée, enregistre et confirme une nouvelle tâche."""
    tache = Tache(
        prochain_id,
        commande.titre,
        commande.priorite,
        commande.echeance,
        commande.etiquettes,
    )
    taches.append(tache)
    depot.enregistrer(taches, prochain_id + 1)
    return 0, f"Tâche {tache.id} ajoutée : {tache.titre}"


def _executer_modification(
    commande: _Terminer | _Supprimer, taches: list[Tache], prochain_id: int, depot: Depot
) -> tuple[int, str]:
    """Termine ou supprime une tâche existante."""
    identifiant = commande.identifiant
    tache = _trouver_tache(taches, identifiant)
    if tache is None:
        return _erreur_tache_introuvable(identifiant)
    if isinstance(commande, _Terminer):
        tache.terminee = True
        message = f"Tâche {identifiant} terminée"
    else:
        taches.remove(tache)
        message = f"Tâche {identifiant} supprimée"
    depot.enregistrer(taches, prochain_id)
    return 0, message


def _trouver_tache(taches: list[Tache], identifiant: int) -> Tache | None:
    """Retourne la tâche portant l'identifiant demandé, si elle existe."""
    return next((tache for tache in taches if tache.id == identifiant), None)


def _erreur_tache_introuvable(identifiant: int) -> tuple[int, str]:
    """Construit la réponse prescrite pour une tâche inexistante."""
    return 1, f"Erreur : tâche {identifiant} introuvable"


def _formater_liste(
    taches: list[Tache],
    toutes: bool = False,
    etiquette: str | None = None,
    priorite: Priorite | None = None,
    date_limite: date | None = None,
) -> str:
    """Filtre, trie et formate les tâches à afficher."""
    selection = [
        tache
        for tache in taches
        if (toutes or not tache.terminee)
        and (etiquette is None or etiquette in tache.etiquettes)
        and (priorite is None or tache.priorite == priorite)
        and (
            date_limite is None
            or (not tache.terminee and tache.echeance is not None and tache.echeance < date_limite)
        )
    ]
    if not selection:
        return "Aucune tâche."
    return "\n".join(_formater_tache(tache) for tache in sorted(selection, key=_cle_tri))


def _cle_tri(tache: Tache) -> tuple[int, bool, date, int]:
    """Construit la clé de tri prescrite par la spécification."""
    return (
        PRIORITES.index(tache.priorite),
        tache.echeance is None,
        tache.echeance or date.max,
        tache.id,
    )


def _formater_tache(tache: Tache) -> str:
    """Formate une tâche sur une ligne."""
    marque = "x" if tache.terminee else " "
    echeance = tache.echeance.isoformat() if tache.echeance is not None else "—"
    etiquettes = "".join(f" #{etiquette}" for etiquette in tache.etiquettes)
    return f"[{marque}] {tache.id}  {tache.priorite:<8} {echeance:>10}  {tache.titre}{etiquettes}"


def _formater_kanban(taches: list[Tache]) -> str:
    """Affiche les tâches dans les colonnes à faire et terminées."""
    a_faire = [tache for tache in taches if not tache.terminee]
    terminees = [tache for tache in taches if tache.terminee]
    return "\n\n".join(
        (
            _formater_colonne_kanban("À faire", a_faire),
            _formater_colonne_kanban("Terminées", terminees),
        )
    )


def _formater_colonne_kanban(titre: str, taches: list[Tache]) -> str:
    """Formate une colonne Kanban avec son nombre de tâches."""
    lignes = [_formater_tache(tache) for tache in sorted(taches, key=_cle_tri)]
    contenu = "\n".join(lignes) if lignes else "Aucune tâche."
    return f"{titre} ({len(taches)})\n{contenu}"


def _exporter_taches(taches: list[Tache], format_export: FormatExport) -> str:
    """Produit un export JSON ou CSV des tâches."""
    taches_triees = sorted(taches, key=_cle_tri)
    if format_export == "json":
        donnees = [
            {
                "id": tache.id,
                "titre": tache.titre,
                "priorite": tache.priorite,
                "echeance": tache.echeance.isoformat() if tache.echeance is not None else None,
                "etiquettes": tache.etiquettes,
                "terminee": tache.terminee,
            }
            for tache in taches_triees
        ]
        return json.dumps(donnees, ensure_ascii=False)
    sortie = io.StringIO(newline="")
    redacteur = csv.writer(sortie, lineterminator="\n")
    redacteur.writerow(["id", "titre", "priorite", "echeance", "etiquettes", "terminee"])
    for tache in taches_triees:
        redacteur.writerow(
            [
                tache.id,
                tache.titre,
                tache.priorite,
                tache.echeance.isoformat() if tache.echeance is not None else "",
                ";".join(tache.etiquettes),
                "oui" if tache.terminee else "non",
            ]
        )
    return sortie.getvalue()
