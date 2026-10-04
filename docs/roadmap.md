# cadrer-x — feuille de route

## Avant la v1

1. Réécrire `docs/vision.md` de cadrer-x sur le Product Vision Board que `cadrer-x-init` produit
   désormais (Vision, Pour qui, Besoins, Produit, Objectifs, Faire ou louer), et le faire valider.
2. Un projet existant sans tests, dont le code suit déjà la disposition de son framework : `ranger`
   n'est pas proposé, donc rien ne fige ce que le produit fait aujourd'hui. Prévoir ce filet (des
   tests du comportement actuel) avant la première fonctionnalité qui touche ce code.
3. Les secrets déjà dans un projet existant : à l'initialisation, les chercher dans les fichiers et
   dans l'historique git (avec un outil d'analyse s'il y en a un), et dire à la personne quoi révoquer
   avant tout le reste.
4. Essayer ces parcours dans le terrain d'essai : une nouvelle fonctionnalité, un petit changement
   visible et un bug (la voie courte élargie et l'entrée des bugs, ajoutées le 2026-10-04), une mise
   en ligne qui échoue et l'initialisation d'un projet existant. Relever les questions inutiles, les
   décisions perdues, les étapes bloquantes et le travail technique laissé à la personne ; corriger
   les compétences d'après ce qu'on y voit.

## Après la v1

- Rendre le dépôt public : la même commande d'installation, avec `curl` au lieu de `gh`.
- Les tests des compétences (evals), refaits sur les compétences de la v1.
- Une compétence d'écriture en français, avec les tics de l'IA à éviter.
- Ajouter le suivi après livraison quand le produit en a besoin : signal à surveiller, seuil d'action,
  personne responsable et chemin pour transformer un problème constaté en correction ou fonctionnalité.
