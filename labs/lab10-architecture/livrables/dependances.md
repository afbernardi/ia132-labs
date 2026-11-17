# Analyse des dépendances legacy

Date d'analyse : 2026-11-17

## Résultat des audits

Les deux ensembles ont été vérifiés avec des outils réels, sans inventer
d'identifiant :

- Python : `pip-audit --disable-pip --no-deps -r requirements-legacy.txt`
- npm : `npm install --package-lock-only`, puis `npm audit`

## Python

`pip-audit` trouve **238 vulnérabilités connues dans 7 paquets**. Ce nombre
inclut des identifiants dupliqués dans plusieurs sources et ne doit pas être
interprété comme 238 vulnérabilités distinctes sans vérification détaillée.

| Paquet | Version | Constats vérifiés | Direction |
|---|---:|---|---|
| django | 2.2.0 | Plusieurs PYSEC, dont les années 2019 à 2026 | Mettre à jour vers une version Django maintenue |
| requests | 2.19.1 | PYSEC-2018-28, PYSEC-2023-74 et alertes ultérieures | Mettre à jour vers au moins 2.32.4 ou une version maintenue compatible |
| urllib3 | 1.24.1 | Plusieurs PYSEC couvrant les versions anciennes | Mettre à jour vers une version 2.x compatible |
| pyyaml | 5.3 | PYSEC-2020-96 et PYSEC-2021-142 | Mettre à jour vers PyYAML 5.4 ou supérieur |
| jinja2 | 2.10 | PYSEC-2019-217, PYSEC-2021-66 et alertes ultérieures | Mettre à jour vers Jinja2 3.1.6 ou supérieur |
| pillow | 8.0.0 | Nombreuses alertes PYSEC, GHSA et CVE | Mettre à jour vers une version récente supportée; valider Python et les API utilisées |
| celery | 4.3.0 | PYSEC-2021-858 | Mettre à jour vers une version maintenue |

Les versions minimales indiquées par `pip-audit` peuvent varier selon une
vulnérabilité donnée. Elles doivent être confirmées dans le rapport complet
avant une montée de version.

## npm

`npm audit` trouve **15 vulnérabilités** :
**3 faibles, 2 modérées, 8 élevées et 2 critiques**.

| Paquet | Rôle | Sévérité npm | Situation |
|---|---|---|---|
| axios | Direct, 0.21.0 | Élevée | Mise à jour disponible vers 0.21.4 |
| express | Direct, 4.16.0 | Élevée | Mise à jour disponible vers 4.22.3 |
| jsonwebtoken | Direct, 8.5.1 | Élevée | Mise à jour majeure vers 9.0.3 |
| lodash | Direct, 4.17.15 | Élevée | Mise à jour disponible vers 4.18.1 |
| moment | Direct, 2.29.1 | Élevée | Mise à jour disponible vers 2.31.0 |
| request | Direct, 2.88.0 | Critique | Aucun correctif disponible; remplacer la dépendance |
| form-data | Transitive | Critique | Aucun correctif direct disponible dans l'audit |
| qs | Transitive | Élevée | Aucun correctif direct disponible dans l'audit |
| tough-cookie | Transitive | Modérée | Aucun correctif direct disponible dans l'audit |
| uuid | Transitive | Modérée | Aucun correctif direct disponible dans l'audit |
| body-parser, cookie, path-to-regexp, send, serve-static | Transitifs | Faible ou élevée selon le paquet | Corrigés par les mises à jour compatibles de Express lorsque possible |

## Décision de réutilisation

La réutilisation directe du prototype ne doit pas être approuvée :

1. Les dépendances Python sont anciennes, incompatibles avec les exigences actuelles
   et présentent une surface de vulnérabilités importante.
2. La pile npm contient deux composants critiques ou difficiles à corriger.
3. Les dépendances directes devront être mises à niveau puis testées avec les
   API utilisées par Cantine+. Une simple mise à jour automatique risquerait
   des changements majeurs, notamment pour `jsonwebtoken`.
4. Le code doit être réévalué indépendamment des manifestations de sécurité;
   l'absence de vulnérabilité connue ne signifie pas l'absence de défaut.

## Identifiants CVE inventés

Aucun identifiant CVE inventé n'a été fourni dans les échanges examinés pour
cette analyse. Les identifiants comme `PYSEC-*`, `GHSA-*` sont les formats
rapportés par les outils; les identifiants `CVE-*` présents dans les résultats
doivent être vérifiés dans la base officielle de la CVE avant toute conclusion.
Toute valeur créée sans résultat d'un outil devra être considérée comme
inexistante jusqu'à vérification.
