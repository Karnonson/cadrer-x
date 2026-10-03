<!--
  Modèle de audit.md cadrer-x : une section par récit, la plus récente en haut. Les titres, libellés et
  préfixes restent tels quels, dans toutes les langues : `realiser` et `rendre` les cherchent par ces
  noms. Le texte est dans la langue de la personne. Les lignes ci-dessous sont des exemples : les
  remplacer toutes. Retirer ces commentaires.
-->

# <Titre> — audit

## US1 <titre du récit>

**Tour** : 1
**Date** : <AAAA-MM-JJ>
**Verdict** : à corriger

### Spec

- Bloquant : src/<module>/api.py:41 — contraire : <ce qui ne va pas> ; <ce qu'une personne rencontre> ; correction : <la correction>
- Info : <une vérification qui tient, en quelques mots>

### Règles

- À corriger : tests/test_<x>.py:30 `<la ligne, citée>` — <ce qui ne va pas> ; <ce qu'une personne rencontre> ; correction : <la correction>
- Info : aucun secret dans le code ni l'historique

### Non jugé

Vérifs : lancées — `<la commande>`, code de sortie 0, « Ran 14 tests … OK »
Écrans : cliqués SC1
- <ce qui n'a pas pu être vérifié, et pourquoi>
