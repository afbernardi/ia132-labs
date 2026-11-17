"""Tests unitaires de l'interface en ligne de commande."""

import json

import pytest

from taches.cli import main


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["ajouter"],
        ["ajouter", "Tâche", "--priorite"],
        ["ajouter", "Tâche", "--priorite", "urgente"],
        ["lister", "--priorite", "urgente"],
        ["lister", "--inconnu"],
        ["terminer", "0"],
        ["terminer", "abc"],
        ["exporter", "--format", "xml"],
        ["en-retard", "--aujourdhui", "2026-02-30"],
    ],
)
def test_retourner_le_code_de_sortie_deux_pour_des_arguments_invalides(tmp_path, argv):
    code, sortie = main(argv, tmp_path / "taches.json")

    assert code == 2
    assert sortie.startswith("Erreur :")


def test_refuser_une_option_non_repetable_dupliquee(tmp_path):
    code, sortie = main(["ajouter", "Tâche", "--priorite", "haute", "--priorite", "basse"], tmp_path / "taches.json")

    assert code == 2
    assert "une fois" in sortie


def test_preserver_le_fichier_si_une_suppression_est_introuvable(tmp_path):
    fichier = tmp_path / "taches.json"
    assert main(["ajouter", "Conserver"], fichier)[0] == 0
    contenu_avant = fichier.read_text(encoding="utf-8")

    resultat = main(["supprimer", "42"], fichier)

    assert resultat == (1, "Erreur : tâche 42 introuvable")
    assert fichier.read_text(encoding="utf-8") == contenu_avant


def test_ajouter_et_lister_preservent_les_espaces_du_titre(tmp_path):
    fichier = tmp_path / "taches.json"
    assert main(["ajouter", "  Tâche  "], fichier) == (0, "Tâche 1 ajoutée :   Tâche  ")

    code, sortie = main(["lister"], fichier)

    assert code == 0
    assert "  Tâche  " in sortie
    assert json.loads(fichier.read_text(encoding="utf-8"))["prochain_id"] == 2


def test_dashbord_kanban_separe_les_taches_a_faire_et_terminees(tmp_path):
    fichier = tmp_path / "taches.json"
    main(["ajouter", "À faire", "--priorite", "haute", "--echeance", "2026-11-05"], fichier)
    main(["ajouter", "Terminée", "--echeance", "2026-11-06"], fichier)
    main(["terminer", "2"], fichier)

    code, sortie = main(["dashbord-kanban"], fichier)

    assert code == 0
    assert sortie == (
        "À faire (1)\n"
        "[ ] 1  haute    2026-11-05  À faire\n\n"
        "Terminées (1)\n"
        "[x] 2  normale  2026-11-06  Terminée"
    )


def test_dashbord_kanban_affiche_les_deux_colonnes_vides(tmp_path):
    code, sortie = main(["dashbord-kanban"], tmp_path / "taches.json")

    assert code == 0
    assert sortie == "À faire (0)\nAucune tâche.\n\nTerminées (0)\nAucune tâche."


def test_dashbord_kanban_refuse_les_arguments(tmp_path):
    code, sortie = main(["dashbord-kanban", "--toutes"], tmp_path / "taches.json")

    assert code == 2
    assert sortie.startswith("Erreur :")
