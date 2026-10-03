# Inscription aux ateliers — tâches

**Source** : `spec.md`, `decisions.md`

## Fondations

aucune

## US1 — S'inscrire à un atelier (Priorité : P1) 🎯

**But** : un membre s'inscrit seul, jamais au-delà des places.

**Test seul** : s'inscrire à un atelier avec des places, puis à un atelier complet.

- [x] T01 [US1] Inscrire un membre à un atelier, dans la limite des places
  - [x] Étant donné un atelier avec une place libre, quand un membre s'inscrit, alors il a une place, et l'atelier a une place libre de moins.
  - [x] Étant donné un atelier complet, quand un membre veut s'inscrire, alors l'inscription est refusée (Complet), et les places libres restent à 0.
  - [x] Étant donné un membre déjà inscrit, quand il s'inscrit encore, alors il a toujours une seule place.
  Exigences : EF1, EF2
  Risques : abus — deux inscriptions en même temps pour la dernière place débordent l'atelier → le compte des places et l'ajout dans une seule transaction ; saisies — un atelier ou un membre inconnu → refusé avant que rien ne soit gardé
  Fichiers : db/migrations/0002_inscriptions.sql, src/clubhouse/signup/__init__.py, src/clubhouse/signup/api.py, tests/test_signup.py
  Après : aucune
  Taille : M

**Point d'étape** : US1 marche seul → `/cadrer-x-examiner US1`.

## US2 — Annuler mon inscription (Priorité : P2)

**But** : rendre sa place jusqu'à 24 heures avant.

**Test seul** : annuler trois jours avant, puis la veille.

- [ ] T02 [US2] Annuler une inscription jusqu'à 24 heures avant
  - [ ] Étant donné un atelier dans plus de 24 heures, quand le membre annule, alors la place redevient libre.
  - [ ] Étant donné un atelier dans moins de 24 heures, quand le membre annule, alors c'est refusé (TropTard), et la place reste prise.
  - [ ] Étant donné l'inscription d'un autre membre, quand un membre essaie de l'annuler, alors c'est refusé (NonAutorise).
  Exigences : EF3
  Risques : données d'un autre — un membre annule l'inscription d'un autre → le membre de l'inscription vérifié contre celui qui demande
  Fichiers : src/clubhouse/signup/cancel.py, tests/test_cancel.py
  Après : T01
  Taille : S

**Point d'étape** : US1 et US2 marchent chacun seul → `/cadrer-x-examiner US2`.

## US3 — Voir qui vient (Priorité : P3)

**But** : la liste des inscrits pour les animateurs.

**Test seul** : demander la liste d'un atelier avec des inscrits.

- [ ] T03 [P] [US3] Donner aux animateurs la liste des inscrits d'un atelier
  - [ ] Étant donné un atelier avec des inscrits, quand un animateur demande la liste, alors il a le nom et l'e-mail de chacun, le premier inscrit d'abord, sans les annulés.
  - [ ] Étant donné un membre qui n'est pas animateur, quand il demande la liste, alors c'est refusé (NonAutorise).
  Exigences : EF4
  Risques : données personnelles — un membre lit les e-mails des autres → le rôle d'animateur vérifié sur le serveur, par l'api.py des membres
  Fichiers : src/clubhouse/signup/attendees.py, tests/test_attendees.py
  Après : T01
  Taille : S

**Point d'étape** : US1, US2 et US3 marchent chacun seul → `/cadrer-x-examiner US3`.

## Ordre

1. Une tâche par session : `/cadrer-x-realiser T<nn>`, chacune dans son worktree. Les tâches `[P]` peuvent tourner en même temps, chacune dans sa session ; les autres attendent ce que nomme leur `Après :`.
2. À chaque point d'étape, la relecture du récit, dans une autre session : `/cadrer-x-examiner US<n>`.
3. Après US1 : la plus petite version qui vaut d'être montrée.
4. Un récit ajouté ne casse jamais ceux d'avant : leurs tests restent verts.

- Vague 1 : T01
- Vague 2 : T02, T03

## À surveiller

- T01 : deux inscriptions au même moment pour la dernière place : une refusée, jamais plus d'inscrits que de places.
- T02 : une annulation à exactement 24 heures du début, et une heure de début gardée avec un autre décalage qu'UTC.

## Couverts

| Quoi | Tâches |
|---|---|
| US1 | T01 |
| US2 | T02 |
| US3 | T03 |
| EF1 | T01 |
| EF2 | T01 |
| EF3 | T02 |
| EF4 | T03 |
| M3 | T02, T03 |
| M6 | T01, T03 |

- Règles en conflit : aucune
