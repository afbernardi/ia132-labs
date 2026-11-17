"""Tests unitaires du modèle des tâches."""

from datetime import date

import pytest

from taches.modele import Tache, convertir_echeance


def test_creer_une_tache_avec_les_valeurs_par_defaut():
    tache = Tache(1, "Préparer la démo")

    assert tache.id == 1
    assert tache.titre == "Préparer la démo"
    assert tache.priorite == "normale"
    assert tache.echeance is None
    assert tache.etiquettes == []
    assert tache.terminee is False


def test_conserver_les_donnees_valides_de_la_tache():
    echeance = date(2026, 11, 5)
    tache = Tache(3, "  Relire le plan  ", "haute", echeance, ["ia", "formation"], True)

    assert tache.titre == "  Relire le plan  "
    assert tache.priorite == "haute"
    assert tache.echeance == echeance
    assert tache.etiquettes == ["ia", "formation"]
    assert tache.terminee is True


@pytest.mark.parametrize("titre", ["", " ", " \t\n"])
def test_refuser_un_titre_vide(titre):
    with pytest.raises(ValueError, match="titre"):
        Tache(1, titre)


@pytest.mark.parametrize("priorite", ["urgente", "", None])
def test_refuser_une_priorite_invalide(priorite):
    with pytest.raises(ValueError, match="priorité"):
        Tache(1, "Tâche", priorite=priorite)


@pytest.mark.parametrize("identifiant", [0, -1, True])
def test_refuser_un_identifiant_non_positif(identifiant):
    with pytest.raises(ValueError, match="identifiant"):
        Tache(identifiant, "Tâche")


def test_convertir_une_echeance_valide():
    assert convertir_echeance("2026-11-05") == date(2026, 11, 5)


def test_convertir_une_echeance_absente():
    assert convertir_echeance(None) is None


@pytest.mark.parametrize("valeur", ["2026-13-05", "2026-02-30", "2026-1-05", "20261105", ""])
def test_refuser_une_echeance_invalide_ou_au_mauvais_format(valeur):
    with pytest.raises(ValueError, match="Échéance"):
        convertir_echeance(valeur)


def test_refuser_une_echeance_dun_type_invalide():
    with pytest.raises(ValueError, match="AAAA-MM-JJ"):
        convertir_echeance(20261105)
