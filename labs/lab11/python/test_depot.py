"""Tests unitaires du dépôt JSON des tâches."""

from datetime import date

import pytest

from taches.depot import Depot
from taches.modele import Tache


def test_charger_un_fichier_absent_retourne_un_depot_vide(tmp_path):
    depot = Depot(tmp_path / "taches.json")

    assert depot.charger() == ([], 1)


def test_enregistrer_puis_charger_une_tache(tmp_path):
    depot = Depot(tmp_path / "taches.json")
    taches = [Tache(1, "Préparer la démo", "haute", date(2026, 11, 5), ["ia"], True)]

    depot.enregistrer(taches, 2)

    assert depot.charger() == (taches, 2)


def test_conserver_le_prochain_identifiant_apres_suppression(tmp_path):
    depot = Depot(tmp_path / "taches.json")
    taches = [Tache(1, "Première"), Tache(3, "Troisième")]
    depot.enregistrer(taches, 4)

    taches_chargees, prochain_id = depot.charger()

    assert [tache.id for tache in taches_chargees] == [1, 3]
    assert prochain_id == 4


def test_refuser_un_prochain_identifiant_deja_utilise(tmp_path):
    depot = Depot(tmp_path / "taches.json")

    with pytest.raises(ValueError, match="supérieur"):
        depot.enregistrer([Tache(2, "Tâche")], 2)


def test_refuser_un_fichier_json_qui_ne_contient_pas_un_objet(tmp_path):
    fichier = tmp_path / "taches.json"
    fichier.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="objet JSON"):
        Depot(fichier).charger()


def test_refuser_des_identifiants_dupliques_dans_le_fichier(tmp_path):
    fichier = tmp_path / "taches.json"
    fichier.write_text(
        '{"prochain_id": 3, "taches": ['
        '{"id": 1, "titre": "A", "priorite": "normale", "echeance": null, "etiquettes": [], "terminee": false},'
        '{"id": 1, "titre": "B", "priorite": "normale", "echeance": null, "etiquettes": [], "terminee": false}'
        ']}',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="double"):
        Depot(fichier).charger()
