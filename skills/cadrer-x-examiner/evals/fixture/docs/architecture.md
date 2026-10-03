# Clubhouse — architecture

## Pièces

- Le programme du club, sur un petit serveur par environnement — Python 3.11, bibliothèque standard ([ADR 0001](adr/0001-stack.md))
- Les données, dans un seul fichier sur ce serveur — SQLite (`data/clubhouse.db`)

## Modules

| Module | Possède | Chemins |
|---|---|---|
| db | la connexion et les migrations | `src/clubhouse/db.py`, `db/migrations/` |
| workshops | les ateliers : titre, date, places | `src/clubhouse/workshops/`, `tests/test_workshops.py` |
| members | les membres : nom, e-mail, rôle (membre ou animateur) | `src/clubhouse/members/`, `tests/test_members.py` |

## Données

- Les ateliers (titre, date, places) : tout le monde les voit.
- Les membres (nom, e-mail, rôle) : les animateurs seulement ; un membre voit les siennes.
- Copié chaque nuit ; on revient à la copie de la veille.

## Secrets

Les variables d'environnement, `.env` en local, jamais commité.

## Coût

Le petit serveur : 5 €/mois.

## En local

`PYTHONPATH=src python3 -m unittest discover -s tests -q`

## Lancer

Les commandes de `cadrer-x.yml`.

## Trajet

Lise ajoute un atelier → le programme le garde → les membres le voient dans la liste.

## À faire

aucun

## Écarté

- Un outil de formulaire en ligne : les données des membres chez un tiers (le club a dit non).

## Mots

- Atelier : une séance datée, avec un nombre de places fixe.
- Place : une place dans un atelier.
- Membre : quelqu'un qui a un compte au club.
- Animateur : un membre qui anime des ateliers.
- Inscription : la place d'un membre dans un atelier. Jamais « réservation ».
