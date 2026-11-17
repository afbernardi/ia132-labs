# Revue de code — service de notes

Fichier examiné : `python/notes_service.py`

| Ligne(s) | Gravité | Problème | Correction proposée | Trouvé par IA | Trouvé par Ruff | Trouvé par moi | Corrigé |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 24, 31 | Bloquant | Les courriels sont interpolés directement dans les requêtes SQL. Une entrée spécialement construite peut modifier la requête et contourner l’authentification. | Paramétrer les deux requêtes avec `?` et transmettre les valeurs séparément. | IA | Oui — S608 (lignes 24 et 31) | — | `2c8e4d1` |
| 23, 29 | Bloquant | Les mots de passe sont hachés avec MD5, sans sel. Cette méthode est rapide et inadaptée au stockage de mots de passe. | Utiliser un hachage dédié et lent avec un sel unique, par exemple `hashlib.pbkdf2_hmac` ou `scrypt`. | IA | Oui — S324 (lignes 23 et 29) | Oui | `b0723ed` |
| 9, 46 | Bloquant | La clé secrète utilisée pour les jetons est inscrite dans le code source. | Lire le secret depuis `NOTES_SECRET` (ou une autre variable d’environnement configurée) et échouer explicitement si elle est absente. | IA | Oui — S105 ligne 9 (pas de signalement à la ligne 46) | Oui | `fc69ae6` |
| 41–43 | Majeur | La lecture d’une note ne vérifie pas que son propriétaire correspond à `user_id`; un utilisateur peut lire une note d’un autre compte s’il connaît son identifiant. | Ajouter `owner = ?` à la requête et fournir `user_id` comme paramètre. | IA | Non | — | `b9b106e` |
| 32–33 | Majeur | `except Exception` masque toutes les erreurs de base de données en les transformant en échec de connexion, ce qui empêche leur diagnostic. | Laisser remonter les erreurs inattendues et ne traiter que les erreurs attendues, de façon explicite. | IA | Non | Oui | — |

## Verdict

**Demander des changements** — les problèmes de sécurité et de contrôle d’accès doivent être corrigés avant approbation.

## À compléter

Les constats ci-dessus proviennent de la revue par l’IA. La commande `ruff check labs/lab07-revue/python` n’était pas disponible directement dans le terminal; `py -m ruff check labs/lab07-revue/python` a été exécutée à la place. Résultat : **5 erreurs** (`S105`, `S324` deux fois et `S608` deux fois), toutes reportées dans la colonne Ruff. Ajouter les constats repérés lors de la revue humaine si nécessaire.
