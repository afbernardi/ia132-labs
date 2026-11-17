import assert from 'node:assert/strict';
import { test } from 'node:test';
import { Panier, StockInsuffisant, type Produit } from './panier.ts';

const produitParDefaut: Produit = { sku: 'KB-01', nom: 'Clavier', prix: 4_999, stock: 10 };

function creerPanier(): Panier {
  return new Panier();
}

test('un panier vide expose les indicateurs à zéro', () => {
  const panier = creerPanier();

  assert.equal(panier.sousTotal(), 0);
  assert.equal(panier.rabais(), 0);
  assert.equal(panier.livraison(), 0);
  assert.equal(panier.total(), 0);
  assert.equal(panier.nombreArticles(), 0);
});

test('ajouter un article par défaut enregistre la quantité et le catalogue', () => {
  const panier = creerPanier();

  panier.ajouter(produitParDefaut);

  assert.deepEqual(panier.lignes, new Map([['KB-01', 1]]));
  assert.deepEqual(panier.catalogue, new Map([['KB-01', produitParDefaut]]));
  assert.equal(panier.nombreArticles(), 1);
});

test('ajouter plusieurs quantités cumule les articles du même produit', () => {
  const panier = creerPanier();

  panier.ajouter(produitParDefaut, 2);
  panier.ajouter(produitParDefaut, 3);

  assert.deepEqual(panier.lignes, new Map([['KB-01', 5]]));
  assert.equal(panier.nombreArticles(), 5);
});

test('refuser une quantité invalide sans modifier le panier', () => {
  const panier = creerPanier();
  panier.ajouter(produitParDefaut);

  assert.throws(() => panier.ajouter(produitParDefaut, 0), { name: 'RangeError' });
  assert.throws(() => panier.ajouter(produitParDefaut, -1), { name: 'RangeError' });
  assert.deepEqual(panier.lignes, new Map([['KB-01', 1]]));
});

test('accepter exactement quatre-vingt-dix-neuf articles', () => {
  const panier = creerPanier();
  const produit = { sku: 'P-99', nom: 'Produit', prix: 100, stock: 99 };

  panier.ajouter(produit, 99);

  assert.deepEqual(panier.lignes, new Map([['P-99', 99]]));
  assert.equal(panier.nombreArticles(), 99);
});

test('refuser cent articles sans modifier le panier', () => {
  const panier = creerPanier();
  const produit = { sku: 'P-99', nom: 'Produit', prix: 100, stock: 100 };

  assert.throws(() => panier.ajouter(produit, 100), { name: 'RangeError' });
  assert.deepEqual(panier.lignes, new Map());
  assert.deepEqual(panier.catalogue, new Map());
});

test('accepter exactement le stock disponible', () => {
  const panier = creerPanier();
  const produit = { sku: 'P-02', nom: 'Produit', prix: 100, stock: 2 };

  panier.ajouter(produit, 2);

  assert.deepEqual(panier.lignes, new Map([['P-02', 2]]));
});

test('refuser d’ajouter un produit sans stock', () => {
  const panier = creerPanier();
  const produit = { sku: 'P-00', nom: 'Produit', prix: 100, stock: 0 };

  assert.throws(() => panier.ajouter(produit), { name: 'StockInsuffisant' });
  assert.deepEqual(panier.lignes, new Map());
  assert.deepEqual(panier.catalogue, new Map());
});

test('refuser tout dépassement du stock sans modifier le panier', () => {
  const panier = creerPanier();

  assert.throws(() => panier.ajouter(produitParDefaut, produitParDefaut.stock + 1), { name: 'StockInsuffisant' });
  assert.deepEqual(panier.lignes, new Map());
  assert.deepEqual(panier.catalogue, new Map());
});

test('retirer une partie des articles met à jour la quantité', () => {
  const panier = creerPanier();
  panier.ajouter(produitParDefaut, 3);

  panier.retirer(produitParDefaut.sku, 1);

  assert.deepEqual(panier.lignes, new Map([['KB-01', 2]]));
  assert.equal(panier.nombreArticles(), 2);
});

test('retirer toute la ligne quand la quantité atteinte ou dépassée', () => {
  for (const quantite of [3, 4]) {
    const panier = creerPanier();
    panier.ajouter(produitParDefaut, 3);

    panier.retirer(produitParDefaut.sku, quantite);

    assert.equal(panier.lignes.has(produitParDefaut.sku), false);
    assert.equal(panier.nombreArticles(), 0);
  }
});

test('retirer sans quantité supprime toute la ligne', () => {
  const panier = creerPanier();
  panier.ajouter(produitParDefaut);

  panier.retirer(produitParDefaut.sku);

  assert.deepEqual(panier.lignes, new Map());
});

test('refuser de retirer un article absent', () => {
  const panier = creerPanier();

  assert.throws(() => panier.retirer('ABSENT'), { name: 'RangeError' });
});

test('appliquer un code promo sans tenir compte de la casse', () => {
  const panier = creerPanier();
  panier.ajouter(produitParDefaut);

  panier.appliquerCode('moins10');
  assert.equal(panier.codePromo, 'MOINS10');
  assert.equal(panier.rabais(), 499);
  assert.equal(panier.livraison(), 799);

  panier.appliquerCode('livraison');
  assert.equal(panier.codePromo, 'LIVRAISON');
  assert.equal(panier.rabais(), 0);
  assert.equal(panier.livraison(), 0);
});

test('refuser un code inconnu sans remplacer le code actif', () => {
  const panier = creerPanier();
  panier.ajouter(produitParDefaut);
  panier.appliquerCode('MOINS10');

  assert.throws(() => panier.appliquerCode('INCONNU'), { name: 'RangeError' });
  assert.equal(panier.codePromo, 'MOINS10');
});

test('calculer le sous-total à partir des prix et des quantités', () => {
  const panier = creerPanier();
  const clavier = { sku: 'KB-01', nom: 'Clavier', prix: 4_999, stock: 5 };
  const souris = { sku: 'MS-01', nom: 'Souris', prix: 1_500, stock: 5 };

  panier.ajouter(clavier, 2);
  panier.ajouter(souris, 1);

  assert.equal(panier.sousTotal(), 11_498);
});

test('calculer le rabais de dix pour cent arrondi au cent', () => {
  const panier = creerPanier();
  const produit = { sku: 'P-01', nom: 'Produit', prix: 4_999, stock: 2 };

  panier.ajouter(produit, 2);
  panier.appliquerCode('MOINS10');

  assert.equal(panier.sousTotal(), 9_998);
  assert.equal(panier.rabais(), 999);
});

test('appliquer le seuil exact de livraison gratuite', () => {
  const panier = creerPanier();

  for (const [prix, livraisonAttendue] of [[4_999, 799], [5_000, 0]] as const) {
    const produit = { sku: 'P-01', nom: 'Produit', prix, stock: 1 };
    panier.ajouter(produit);
    assert.equal(panier.livraison(), livraisonAttendue);
    panier.retirer('P-01');
  }
});

test('appliquer le seuil de livraison après le rabais', () => {
  const panier = creerPanier();

  for (const [prix, livraisonAttendue] of [[5_554, 799], [5_555, 0]] as const) {
    const produit = { sku: 'P-01', nom: 'Produit', prix, stock: 1 };
    panier.ajouter(produit);
    panier.appliquerCode('MOINS10');
    assert.equal(panier.livraison(), livraisonAttendue);
    panier.retirer('P-01');
    panier.codePromo = null;
  }
});

test('calculer le total avec rabais et frais de livraison', () => {
  const panier = creerPanier();
  const produit = { sku: 'P-01', nom: 'Produit', prix: 1_000, stock: 1 };

  panier.ajouter(produit);
  panier.appliquerCode('MOINS10');

  assert.equal(panier.total(), 1_699);
});

test('ne pas facturer la livraison d’un panier vide avec un code', () => {
  const panier = creerPanier();

  panier.appliquerCode('LIVRAISON');

  assert.equal(panier.livraison(), 0);
  assert.equal(panier.total(), 0);
});
