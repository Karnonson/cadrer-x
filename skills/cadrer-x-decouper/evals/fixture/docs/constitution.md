# Carnet — constitution

Les règles que chaque changement respecte. Une règle ne change que par un ADR approuvé (`docs/adr/`).

| # | Règle | Vérifiée par | Quand |
|---|---|---|---|
| M1 | Un membre ne voit et ne change que ses notes et ses réglages ; celles d'un autre répondent « introuvable » | des tests d'abus ; la relecture | construction ; relecture |
| M2 | Chaque saisie (formulaire, lien, requête) est vérifiée sur le serveur : type, longueur, forme | les tests de la tâche ; la relecture | construction ; relecture |
| M3 | Aucun secret dans le dépôt, un journal ou une erreur qu'un membre voit | la relecture | construction ; relecture |
| M4 | Les écrans n'utilisent que les parties et les tokens du design system (en code : `src/components/`, `src/styles/tokens.css`) ; une partie qui manque est listée dans la passation, avec pourquoi | la relecture | maquette ; construction ; relecture |
| M5 | Chaque texte qu'un membre lit est en français et suit `docs/textes.md` | la relecture | maquette ; construction ; relecture |
| M6 | Téléphone d'abord : chaque écran marche à 390 px de large sans défiler de côté | la relecture, dans un navigateur | maquette ; relecture |

## Exceptions

aucune
