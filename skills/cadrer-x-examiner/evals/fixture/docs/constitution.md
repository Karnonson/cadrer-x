# Clubhouse — constitution

Les règles que chaque changement respecte. Une règle ne change que par un ADR approuvé (`docs/adr/`).

| # | Règle | Vérifiée par | Quand |
|---|---|---|---|
| M1 | Aucun secret dans le dépôt, un commit ou une sortie affichée | la relecture | chaque tâche ; la relecture |
| M2 | Chaque saisie d'une personne est vérifiée avant d'être utilisée | les tests de la tâche ; la relecture | construction ; relecture |
| M3 | Un membre ne voit et ne change que ses inscriptions et ses données ; les animateurs voient celles de leurs ateliers | des tests d'abus ; la relecture | construction ; relecture |
| M4 | Chaque donnée personnelle est listée dans `docs/security/data-inventory.md`, avec sa base légale et sa durée, avant d'être gardée | le découpage ; la livraison | découpage ; livraison |
| M5 | Bibliothèque standard seulement : une nouvelle dépendance demande un ADR | la relecture | relecture |
| M6 | Un module n'en utilise un autre que par son `api.py` | la relecture | relecture |

## Exceptions

aucune
