# Mesures avant / après optimisation

Temps mesurés avec `python labs/lab05-performance/python/bench.py`. Les valeurs
avant proviennent de la capture initiale; les valeurs après ont été relevées
après l'optimisation. Les temps sont en secondes et peuvent varier selon la
machine.

| Fonction | Taille | Avant (s) | Après (s) |
| --- | ---: | ---: | ---: |
| `dedoublonner` | 2 000 | 0,031 | 0,001 |
| `dedoublonner` | 4 000 | 0,114 | 0,001 |
| `dedoublonner` | 8 000 | 0,473 | 0,002 |
| `top_domaines` | 2 000 | 0,010 | 0,001 |
| `top_domaines` | 4 000 | 0,021 | 0,002 |
| `top_domaines` | 8 000 | 0,040 | 0,003 |
| `communs` | 2 000 | 0,095 | 0,001 |
| `communs` | 4 000 | 0,346 | 0,002 |
| `communs` | 8 000 | 1,873 | 0,005 |
