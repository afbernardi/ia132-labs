"""Tests d'intégration : un VRAI serveur HTTP, de vraies requêtes.

La fixture `serveur` démarre l'API sur un port libre et l'arrête à la fin du module.
Scénarios : santé, création/redirection, statistiques, entrées invalides,
codes/routes inconnus et 200 créations concurrentes.
"""

from concurrent.futures import ThreadPoolExecutor
import json
import threading
import urllib.error
import urllib.request

import pytest

from api import creer_serveur


class SansRedirection(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None  # pour lire la réponse 302 elle-même


ouvrir = urllib.request.build_opener(SansRedirection).open


@pytest.fixture(scope="module")
def serveur():
    srv = creer_serveur()
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


def requete(base, methode, chemin, corps=None):
    """Retourne la réponse sans lever d'exception sur 4xx; envoie les octets tels quels."""
    if isinstance(corps, bytes):
        donnees = corps
    elif corps is not None:
        donnees = json.dumps(corps).encode()
    else:
        donnees = None
    req = urllib.request.Request(base + chemin, data=donnees, method=methode, headers={"Content-Type": "application/json"})
    try:
        with ouvrir(req, timeout=5) as r:
            brut = r.read()
            return r.status, r.headers, json.loads(brut) if brut else None
    except urllib.error.HTTPError as e:
        brut = e.read()
        return e.code, e.headers, json.loads(brut) if brut else None


def test_sante(serveur):
    statut, _, corps = requete(serveur, "GET", "/sante")
    assert (statut, corps) == (200, {"statut": "ok"})


def test_creation_puis_redirection(serveur):
    url = "https://exemple.ca/ressource"
    statut, _, corps = requete(serveur, "POST", "/liens", {"url": url})

    assert statut == 201
    assert corps is not None
    assert corps["url"] == url
    code = corps["code"]

    statut, entetes, corps = requete(serveur, "GET", f"/l/{code}")
    assert statut == 302
    assert entetes["Location"] == url
    assert corps is None


def test_statistiques_apres_trois_visites(serveur):
    url = "https://exemple.ca/statistiques"
    statut, _, creation = requete(serveur, "POST", "/liens", {"url": url})
    assert statut == 201
    assert creation is not None
    code = creation["code"]

    for _ in range(3):
        statut, entetes, _ = requete(serveur, "GET", f"/l/{code}")
        assert statut == 302
        assert entetes["Location"] == url

    statut, _, stats = requete(serveur, "GET", f"/stats/{code}")
    assert (statut, stats) == (
        200,
        {"code": code, "url": url, "clics": 3},
    )


@pytest.mark.parametrize(
    "corps",
    [
        {"url": "ftp://exemple.ca"},
        {"url": "https://"},
        {"url": ""},
        {"url": None},
        {},
    ],
)
def test_url_invalide_retourne_400(serveur, corps):
    statut, _, reponse = requete(serveur, "POST", "/liens", corps)

    assert (statut, reponse) == (
        400,
        {"erreur": "url invalide : http(s)://… attendu"},
    )


def test_json_mal_forme_retourne_400(serveur):
    statut, _, corps = requete(serveur, "POST", "/liens", b'{"url":')

    assert (statut, corps) == (400, {"erreur": "JSON invalide"})


def test_code_inconnu_retourne_404(serveur):
    statut_redirection, _, erreur_redirection = requete(
        serveur, "GET", "/l/code-inconnu"
    )
    statut_stats, _, erreur_stats = requete(
        serveur, "GET", "/stats/code-inconnu"
    )

    assert (statut_redirection, erreur_redirection) == (
        404,
        {"erreur": "lien inconnu"},
    )
    assert (statut_stats, erreur_stats) == (404, {"erreur": "lien inconnu"})


def test_route_inconnue_retourne_404(serveur):
    statut, _, corps = requete(serveur, "GET", "/route-inconnue")

    assert (statut, corps) == (404, {"erreur": "route inconnue"})


def test_200_creations_concurrentes_produisent_200_codes_uniques(serveur):
    with ThreadPoolExecutor(max_workers=200) as executant:
        resultats = list(
            executant.map(
                lambda index: requete(
                    serveur,
                    "POST",
                    "/liens",
                    {"url": f"https://exemple.ca/concurrent/{index}"},
                ),
                range(200),
            )
        )

    assert len(resultats) == 200
    assert all(statut == 201 and corps is not None for statut, _, corps in resultats)
    codes = [corps["code"] for _, _, corps in resultats]
    assert len(set(codes)) == 200
