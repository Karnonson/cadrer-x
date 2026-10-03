# 0001 — Stack : la bibliothèque standard de Python et SQLite

## Contexte
Deux animateurs bénévoles font tourner le club ; personne ne s'occupe de serveurs ni de dépendances à plein temps.

## Décision
Python 3.11+, bibliothèque standard seulement, SQLite dans un seul fichier.

## Options
- Python et SQLite : rien à installer, un fichier à copier.
- Un framework web et PostgreSQL : plus de fonctions, un serveur de base à faire tourner.
- Un outil de formulaire en ligne : pas de code, mais les données des membres chez un tiers (le club a dit non).

## Pourquoi
Rien à mettre à jour que Python ; toute la base tient dans un fichier que la copie de nuit emporte.
