# Registre des risques — Cantine+

| ID | Risque | Probabilité | Impact | Mesure |
|---|---|---|---|---|
| R1 | Informations d'allergènes incorrectes ou obsolètes | Moyenne | Critique | Mise en place d'une revue obligatoire avant publication, d'une piste d'audit complète, de la version affichée dans chaque commande et de tests de régression sur les listes d'allergènes |
| R2 | Charge supérieure aux capacités lors du pic de 1 500 commandes | Moyenne | Critique | Faire un test de charge sur la fenêtre 9 h 45–10 h 30, ajouter un cache pour les menus, surveiller la base et dimensionner les créneaux avant le pilote |
| R3 | Import SAP incomplet ou ancien lors de la synchronisation nocturne | Moyenne | Élevé | Journaliser chaque lot, conserver horodatage et nombre d'erreurs, rejouer les imports échoués et bloquer les retenues non vérifiables |
| R4 | Indisponibilité du prestataire de paiement | Faible | Élevé | Mettre en attente le paiement explicitement, limiter les appels synchrones, utiliser des retries bornés et prévoir une annulation ou une reprise idempotente |
| R5 | Dépassement de la capacité des créneaux de cuisine | Moyenne | Élevé | Vérifier atomiquement la capacité dans la même transaction que la commande, bloquer les surplus et permettre seulement des créneaux disponibles |
| R6 | Fuite ou mauvaise conservation des données personnelles | Moyenne | Critique | Appliquer minimisation des données, chiffrement au repos et en transit, rôles Entra ID stricts, conservation d'un an et procédures de suppression et d'audit |
| R7 | Indisponibilité ou retard des notifications | Moyenne | Moyen | Passer les notifications par une file asynchrone avec reprise, conserver leur état et fournir un repli dans l'application |
| R8 | Évolution du périmètre pilote ou choix tardif du paiement | Élevée | Élevé | Figer le périmètre pilote Laval avant le sprint 2, limiter le MVP aux fonctions essentielles et obtenir une décision rapide sur le prestataire de paiement |
| R9 | Module monolithique devenu trop couplé | Moyenne | Élevé | Définir des interfaces internes explicites, appliquer des limites de dépendances, faire des revues architecturales et extraire seulement les modules dont le besoin est démontré |
