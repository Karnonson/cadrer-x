# cadrer-x — feuille de route

## Pour la v2

0. Corriger ce que les essais de la v1 ont montré, dans l'ordre du verdict
   (`docs/reports/2026-10-06-verdict.md`, sur la branche `skills/session-audit-oct06`).

1. Réécrire `docs/vision.md` de cadrer-x sur le Product Vision Board que `cadrer-x-init` produit
   désormais (Vision, Pour qui, Besoins, Produit, Objectifs, Faire ou louer), et le faire valider.
2. Un projet existant sans tests, dont le code suit déjà la disposition de son framework : `ranger`
   n'est pas proposé, donc rien ne fige ce que le produit fait aujourd'hui. Prévoir ce filet (des
   tests du comportement actuel) avant la première fonctionnalité qui touche ce code.
3. Les secrets déjà dans un projet existant : à l'initialisation, les chercher dans les fichiers et
   dans l'historique git (avec un outil d'analyse s'il y en a un), et dire à la personne quoi révoquer
   avant tout le reste.
4. Le parcours entier, de `init` à la mise en ligne, sur trois projets. Y passer aussi une nouvelle
   fonctionnalité, un petit changement visible et un bug (la voie courte élargie et l'entrée des bugs,
   ajoutées le 2026-10-04), une mise en ligne qui échoue et l'initialisation d'un projet existant.
   Relever les questions inutiles, les décisions perdues, les étapes bloquantes et le travail
   technique laissé à la personne ; corriger les compétences d'après ce qu'on y voit.
5. La v2 : une fois ces essais validés par le propriétaire, publier `v2.0.0` sur GitHub (une release,
   avec ce qu'elle contient).

## Après la v2

- Un hook git avant chaque commit qui lance `tools/status_check.py`, si `STATUS.md` grossit malgré
  ses règles pendant les essais.
- Rendre le dépôt public : la même commande d'installation, avec `curl` au lieu de `gh`.
- L'installation prend la dernière version publiée (le dernier tag `vX.Y.Z`) et non plus `main` ; une
  option en choisit une autre (`--version v1.0.0`). Relancer la commande passe à la dernière version.
- Dire dans le README ce que veut dire chaque numéro de `vX.Y.Z` : X change quand un projet commencé
  avec l'ancienne version doit être adapté (un nom de fichier, un titre, une étape qui change) ; Y,
  quand une étape ou une aide arrive sans rien casser ; Z, pour une correction.
- Les tests des compétences (evals), refaits sur les compétences de la v2.
- Une compétence d'écriture en français, avec les tics de l'IA à éviter.
- Ajouter le suivi après livraison quand le produit en a besoin : signal à surveiller, seuil d'action,
  personne responsable et chemin pour transformer un problème constaté en correction ou fonctionnalité.
- Apprendre d'une session à l'autre : les corrections de la personne, une règle d'écart qui se
  déclenche souvent et les corrections automatiques des vérifs deviennent des leçons du projet
  (`.cadrer-x/lecon.md`), lues par les sessions suivantes et jointes aux tâches qu'elles concernent,
  pour que la même erreur ne soit pas réapprise à chaque fonctionnalité.

## Idées en attente

- Des techniques de remue-méninges dans `choisir` : SCAMPER, le remue-méninges inversé, lever une
  contrainte, et trois autres méthodes structurées, avec une protection contre les biais.
- Reconnaître seul un projet existant et en écrire l'analyse avant le premier entretien.
