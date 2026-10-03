<!--
  Modèle de taches.md cadrer-x, adapté du modèle de tâches de spec-kit
  (https://github.com/github/spec-kit/blob/main/templates/tasks-template.md, licence MIT, © GitHub, Inc.).
  Les titres, libellés et identifiants restent tels quels, dans toutes les langues : `realiser`,
  `examiner` et `rendre` les cherchent par ces noms. Le texte est dans la langue de la personne.
  Les tâches ci-dessous sont des exemples : les remplacer toutes. Retirer ces commentaires.
-->

# <Titre> — tâches

**Source** : `spec.md`, `decisions.md`, `passation.md` (s'il y a des écrans)

## Format

`- [ ] T01 [P] [US1] <verbe> <ce qu'elle construit>`, puis ses lignes :

- `- [ ] <fait quand>` : un scénario de la spec, comme la vérification que le test de la tâche prouve.
  Chaque scénario de `spec.md` est la case d'une seule tâche ; une case qu'aucun scénario ne demande
  est du hors-champ.
- `Exigences :` les `EF<n>` de la spec que la tâche rend vraies.
- `Risques :` <domaine> — <menace> → <protection> ; … ou `aucun — <pourquoi>`. Un test par risque.
- `Écrans :` les `SC<n>` de `passation.md` qu'elle construit ou change ; pas de ligne sans écran.
- `Fichiers :` les chemins exacts, tests compris ; la tâche ne touche qu'eux.
- `Après :` les tâches sans lesquelles elle ne se construit ni ne se teste, ou `aucune`.
- `Taille :` XS (1 fichier), S (1–2), M (3–5). Au-delà, ou un « et » dans le titre : deux tâches.
- `[P]` : elle peut se construire en même temps que la tâche d'avant (son `Après :` ne la nomme pas,
  et elles n'ont aucun fichier en commun).

Chaque tâche est une tranche fine qui traverse toutes les couches dont elle a besoin (ce qu'on garde,
la règle, ce qu'on voit) et qu'un test prouve, jamais une couche seule (« la table », « les routes »).
Le test s'écrit en premier, dans la tâche elle-même : pas de tâche de tests à part.

## Fondations

<!--
  Seulement ce dont le premier récit a besoin en dessous et que plusieurs tâches partagent : un outil
  de test absent, une migration, le dossier d'un module. Rien qui ne serve aucun récit. Vide : `aucune`.
-->

- [ ] T01 [US1] <verbe> <ce que les récits partagent>
  - [ ] <fait quand>
  Exigences : aucune
  Risques : aucun — <pourquoi>
  Fichiers : <chemin>, <chemin>
  Après : aucune
  Taille : S

---

## US1 — <titre> (Priorité : P1) 🎯

**But** : <ce que ce récit apporte, en une ligne>

**Test seul** : <comment le vérifier seul, repris de spec.md>

- [ ] T02 [US1] <verbe> <le chemin le plus fin de bout en bout>
  - [ ] Étant donné <…>, quand <…>, alors <…>
  Exigences : EF1
  Risques : <domaine> — <menace> → <protection>
  Écrans : SC1
  Fichiers : <chemin>, <le fichier de test>
  Après : T01
  Taille : M
- [ ] T03 [P] [US1] <verbe> <un état de plus : vide, erreur>
  - [ ] Étant donné <…>, quand <…>, alors <…>
  Exigences : EF2
  Risques : aucun — <pourquoi>
  Écrans : SC1
  Fichiers : <chemin>, <le fichier de test>
  Après : T01
  Taille : S

**Point d'étape** : US1 marche seul → `/cadrer-x-examiner US1`.

---

## US2 — <titre> (Priorité : P2)

**But** : <…>

**Test seul** : <…>

- [ ] T04 [US2] <verbe> <…>
  - [ ] Étant donné <…>, quand <…>, alors <…>
  Exigences : EF3
  Risques : <…>
  Fichiers : <…>
  Après : T02
  Taille : S

**Point d'étape** : US1 et US2 marchent chacun seul → `/cadrer-x-examiner US2`.

---

<!-- Un bloc par récit, dans l'ordre des priorités de spec.md. -->

## Ordre

1. Une tâche par session : `/cadrer-x-realiser T<nn>`, chacune dans son worktree. Les tâches `[P]`
   peuvent tourner en même temps, chacune dans sa session ; les autres attendent ce que nomme leur `Après :`.
2. À chaque point d'étape, la relecture du récit, dans une autre session : `/cadrer-x-examiner US<n>`.
3. Après US1 : la plus petite version qui vaut d'être montrée. On peut s'arrêter là et la montrer.
4. Un récit ajouté ne casse jamais ceux d'avant : leurs tests restent verts.

## À surveiller

<!--
  Jusqu'à cinq cas que la spec implique et qu'aucune case ne teste (le même moment, une limite, une
  valeur hostile, une liste vide), chacun épinglé à la tâche qui porte le code. `- aucun` seulement
  après avoir cherché.
-->

- T02 : <un échec que la spec implique et qu'aucun test de tâche ne couvre>

## Couverts

<!--
  La vérification finale du découpage : chaque récit, chaque exigence de la spec, et chaque règle de
  la constitution qui demande à cette fonctionnalité un test ou un outil (`M<n>`), avec les tâches qui
  les couvrent. Une règle que la spec oblige à enfreindre va sous Règles en conflit, avec sa question
  dans `a-trancher.md`.
-->

| Quoi | Tâches |
|---|---|
| US1 | T01, T02, T03 |
| US2 | T04 |
| EF1 | T02 |
| EF2 | T03 |
| EF3 | T04 |
| M4 | T01 |

- Règles en conflit : aucune
