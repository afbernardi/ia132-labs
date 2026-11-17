"""Tests unitaires du panier d'achat."""

import pytest

from panier import Panier, Produit, StockInsuffisant


@pytest.fixture
def produit():
    return Produit("KB-01", "Clavier", 4_999, stock=10)


@pytest.fixture
def panier():
    return Panier()


@pytest.fixture
def panier_avec_produit(panier, produit):
    panier.ajouter(produit)
    return panier


def test_panier_vide_a_tous_les_indicateurs_nuls(panier):
    assert panier.sous_total() == 0
    assert panier.rabais() == 0
    assert panier.livraison() == 0
    assert panier.total() == 0
    assert panier.nombre_articles() == 0


def test_ajouter_un_article_par_defaut(panier, produit):
    panier.ajouter(produit)

    assert panier.lignes == {"KB-01": 1}
    assert panier.catalogue == {"KB-01": produit}
    assert panier.nombre_articles() == 1


def test_ajouter_des_quantites_cumulees(panier, produit):
    panier.ajouter(produit, 2)
    panier.ajouter(produit, 3)

    assert panier.lignes == {"KB-01": 5}
    assert panier.nombre_articles() == 5


@pytest.mark.parametrize("quantite", [0, -1])
def test_refuser_une_quantite_invalide_sans_modifier_le_panier(panier_avec_produit, produit, quantite):
    with pytest.raises(ValueError):
        panier_avec_produit.ajouter(produit, quantite)

    assert panier_avec_produit.lignes == {"KB-01": 1}


def test_accepter_exactement_quatre_vingt_dix_neuf_articles(panier):
    produit = Produit("P-99", "Produit", 100, stock=99)

    panier.ajouter(produit, 99)

    assert panier.lignes == {"P-99": 99}
    assert panier.nombre_articles() == 99


def test_refuser_cent_articles_sans_modifier_le_panier(panier):
    produit = Produit("P-99", "Produit", 100, stock=100)

    with pytest.raises(ValueError):
        panier.ajouter(produit, 100)

    assert panier.lignes == {}
    assert panier.catalogue == {}


def test_accepter_exactement_le_stock_disponible(panier):
    produit = Produit("P-02", "Produit", 100, stock=2)

    panier.ajouter(produit, 2)

    assert panier.lignes == {"P-02": 2}


def test_refuser_ajouter_un_produit_sans_stock(panier):
    produit = Produit("P-00", "Produit", 100, stock=0)

    with pytest.raises(StockInsuffisant):
        panier.ajouter(produit)

    assert panier.lignes == {}
    assert panier.catalogue == {}


def test_refuser_de_depassement_du_stock_sans_modifier_le_panier(panier, produit):
    with pytest.raises(StockInsuffisant):
        panier.ajouter(produit, produit.stock + 1)

    assert panier.lignes == {}
    assert panier.catalogue == {}


def test_retirer_une_partie_des_articles(panier, produit):
    panier.ajouter(produit, 3)

    panier.retirer(produit.sku, 1)

    assert panier.lignes == {"KB-01": 2}
    assert panier.nombre_articles() == 2


@pytest.mark.parametrize("quantite", [3, 4])
def test_retirer_toute_la_ligne_si_la_quantite_est_atteinte_ou_depassee(panier, produit, quantite):
    panier.ajouter(produit, 3)

    panier.retirer(produit.sku, quantite)

    assert produit.sku not in panier.lignes
    assert panier.nombre_articles() == 0


def test_retirer_sans_quantite_supprime_toute_la_ligne(panier_avec_produit, produit):
    panier_avec_produit.retirer(produit.sku)

    assert panier_avec_produit.lignes == {}


def test_refuser_de_retirer_un_article_absent(panier):
    with pytest.raises(KeyError):
        panier.retirer("ABSENT")


@pytest.mark.parametrize(
    ("code", "code_attendu", "rabais_attendu", "livraison_attendue"),
    [
        ("moins10", "MOINS10", 499, 799),
        ("livraison", "LIVRAISON", 0, 0),
    ],
)
def test_appliquer_un_code_promo_sans_tenir_compte_de_la_casse(
    panier, produit, code, code_attendu, rabais_attendu, livraison_attendue
):
    panier.ajouter(produit)

    panier.appliquer_code(code)

    assert panier.code_promo == code_attendu
    assert panier.rabais() == rabais_attendu
    assert panier.livraison() == livraison_attendue


def test_refuser_un_code_inconnu_sans_remplacer_le_code_actif(panier_avec_produit):
    panier_avec_produit.appliquer_code("MOINS10")

    with pytest.raises(ValueError):
        panier_avec_produit.appliquer_code("INCONNU")

    assert panier_avec_produit.code_promo == "MOINS10"


def test_calculer_le_sous_total_a_partir_des_prix_et_quantites(panier):
    clavier = Produit("KB-01", "Clavier", 4_999, stock=5)
    souris = Produit("MS-01", "Souris", 1_500, stock=5)
    panier.ajouter(clavier, 2)
    panier.ajouter(souris, 1)

    assert panier.sous_total() == 11_498


def test_calculer_le_rabais_de_dix_pourcent_arrondi_au_cent(panier):
    produit = Produit("P-01", "Produit", 4_999, stock=2)
    panier.ajouter(produit, 2)
    panier.appliquer_code("MOINS10")

    assert panier.sous_total() == 9_998
    assert panier.rabais() == 999


@pytest.mark.parametrize(
    ("prix", "livraison_attendue"),
    [
        (4_999, 799),
        (5_000, 0),
    ],
)
def test_appliquer_le_seuil_exact_de_livraison_gratuite(panier, prix, livraison_attendue):
    produit = Produit("P-01", "Produit", prix, stock=1)
    panier.ajouter(produit)

    assert panier.livraison() == livraison_attendue


@pytest.mark.parametrize(
    ("prix", "livraison_attendue"),
    [
        (5_554, 799),
        (5_555, 0),
    ],
)
def test_appliquer_le_seuil_de_livraison_apres_le_rabais(panier, prix, livraison_attendue):
    produit = Produit("P-01", "Produit", prix, stock=1)
    panier.ajouter(produit)
    panier.appliquer_code("MOINS10")

    assert panier.livraison() == livraison_attendue


def test_calculer_le_total_avec_rabais_et_frais_de_livraison(panier):
    produit = Produit("P-01", "Produit", 1_000, stock=1)
    panier.ajouter(produit)
    panier.appliquer_code("MOINS10")

    assert panier.total() == 1_699


def test_ne_pas_facturer_la_livraison_dun_panier_vide_avec_un_code(panier):
    panier.appliquer_code("LIVRAISON")

    assert panier.livraison() == 0
    assert panier.total() == 0
