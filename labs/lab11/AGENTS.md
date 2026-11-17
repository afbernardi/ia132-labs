# Instructions pour l’agent · projet `taches`

Ce fichier décrit les consignes de travail pour le gestionnaire de tâches du lab 11.
La spécification fait foi : `SPEC.md`.

## Le projet

Gestionnaire de tâches en ligne de commande, implémenté en Python ou en TypeScript.
Chaque commande lit les données JSON, effectue l’opération et enregistre le résultat.

## Commandes

- Depuis la racine du dépôt, tests Python : `pytest labs/lab11/python`
- Tests TypeScript : `node --test labs/lab11/typescript/acceptation.test.ts`
- Après l’ajout de tests TypeScript, suite complète : `node --test "labs/lab11/typescript/**/*.test.ts"`
- Vérification Ruff : `ruff check labs/lab11/python`
- Lancer Python : `cd labs/lab11/python && python -m taches lister`
- Lancer TypeScript : `node labs/lab11/typescript/taches/cli.ts lister`

Les tests d’acceptation sont volontairement rouges au départ. Exécuter les tests ciblés
après chaque incrément, examiner les échecs et les corriger avant de poursuivre. Le script
`npm run test:lab11` cible `labs/lab11-projet-final`, pas cette copie.

## Architecture

- `python/taches/modele.py` et `typescript/taches/modele.ts` : modèle et règles métier d’une tâche.
- `python/taches/depot.py` et `typescript/taches/depot.ts` : lecture et écriture du fichier JSON.
- `python/taches/cli.py` et `typescript/taches/cli.ts` : validation des arguments, exécution des commandes et formatage des sorties.
- `python/test_acceptation.py` et `typescript/acceptation.test.ts` : tests d’acceptation de `SPEC.md`, à garder intacts.
- Ajouter les tests unitaires dans des fichiers distincts, par exemple `python/test_modele.py` et `typescript/taches/modele.test.ts`.

## Conventions

- Suivre `SPEC.md` pour les commandes, les sorties, les codes de retour et les règles métier.
- Garder les modules séparés selon leurs responsabilités : modèle, dépôt de données et interface en ligne de commande.
- Écrire le code, les noms et les commentaires en français; ne pas utiliser d’accents dans les identifiants.
- Python : respecter PEP 8, annoter les types, utiliser des docstrings Google et faire passer Ruff.
- TypeScript : conserver le mode strict, éviter `any` et documenter les fonctions exportées avec TSDoc.
- Utiliser uniquement la bibliothèque standard; persister les données dans le JSON défini par la spécification.
- La fonction `main` reçoit les arguments sans le nom du programme et retourne le code et le texte de sortie; elle ne doit pas appeler `sys.exit`.
- Valider les entrées et signaler les erreurs conformément aux codes et messages prescrits par `SPEC.md`.

## Règles strictes

- Ne jamais modifier `python/test_acceptation.py` ni `typescript/acceptation.test.ts` pour faire passer l’implémentation.
- Ne pas affaiblir ou supprimer un test; ajouter au moins cinq tests unitaires ciblés dans des fichiers séparés.
- Aucune dépendance externe : bibliothèque standard uniquement.
- Ne pas modifier les fichiers hors de `labs/lab11` sans demande explicite.
- Ne pas écrire toute l’application d’un seul coup : proposer un plan avant le code, puis avancer commande par commande.
- Ne pas appeler `sys.exit` dans `main` ni remplacer les codes de sortie spécifiés par des exceptions ou des sorties différentes.
- Lancer les tests pertinents après chaque incrément; ne pas ignorer un échec ni poursuivre sans l’avoir compris.

## Avant de terminer une tâche

- [ ] Tests Python et/ou TypeScript pertinents exécutés et réussis.
- [ ] `ruff check labs/lab11/python` réussi pour les changements Python.
- [ ] Tests d’acceptation inchangés et au moins cinq tests unitaires ajoutés.
- [ ] Aucun changement hors du lab et aucune dépendance ajoutée.
- [ ] Exemples et commandes de la documentation vérifiés.
