# Recherche dans les notes — spec

**Branche** : `feature/recherche-notes`
**Créée** : 2026-10-01
**Statut** : validée
**Source** : `idee.md`, `decisions.md`

## Récits

### US1 — Retrouver mes notes par un mot (Priorité : P1)

En tant que membre, je veux taper un mot et voir mes notes qui le contiennent afin de retrouver une citation avant la réunion de mon club.

**Pourquoi cette priorité** : c'est tout le problème de l'idée.

**Test seul** : se vérifie entièrement en cherchant « jardin » dans un compte qui a des notes, et apporte déjà de quoi retrouver une citation.

**Scénarios** :

1. **Étant donné** trois de mes notes qui contiennent « jardin », **quand** je tape « jardin », **alors** je les vois, la plus récente d'abord, chacune avec le titre de son livre et les mots autour.
2. **Étant donné** une note qui dit « Été », **quand** je tape « ete », **alors** je la vois aussi.
3. **Étant donné** qu'aucune de mes notes ne contient le mot, **quand** je le cherche, **alors** on me le dit, avec le mot que j'ai tapé.
4. **Étant donné** que la recherche ne peut pas se faire, **quand** je cherche, **alors** on me dit de réessayer, et ce que j'ai tapé est toujours là.
5. **Étant donné** la note d'un autre membre qui contient « jardin », **quand** je tape « jardin », **alors** je ne la vois jamais.

---

### US2 — Lire une note trouvée (Priorité : P2)

En tant que membre, je veux ouvrir une note depuis les résultats afin de la lire en entier et d'en copier la citation.

**Pourquoi cette priorité** : sans elle, on voit seulement quelques mots autour.

**Test seul** : se vérifie en touchant un résultat puis en revenant aux résultats.

**Scénarios** :

1. **Étant donné** mes résultats, **quand** je touche l'un d'eux, **alors** je vois la note entière, son livre, et sa page si je l'ai notée.
2. **Étant donné** une note ouverte depuis les résultats, **quand** je reviens en arrière, **alors** je retrouve mes résultats sans retaper le mot.

### Cas limites

- Un texte de plus de 100 caractères : on garde les 100 premiers.
- Une note d'un autre membre ouverte par son adresse : « introuvable » (M1).

## Exigences

- **EF1** : L'appli DOIT chercher le mot dans le texte des notes du membre seulement, pas dans les titres des livres.
- **EF2** : L'appli DOIT trouver le mot sans tenir compte des accents ni des majuscules.
- **EF3** : L'appli DOIT montrer les résultats de la note la plus récente à la plus ancienne.
- **EF4** : L'appli DOIT accepter au plus 100 caractères dans la recherche.
- **EF5** : L'appli NE DOIT garder aucune trace des recherches.

## Critères

- **CS1** : D'ici le 31 janvier 2027, 30 % des membres actifs chaque semaine cherchent au moins une fois par semaine.

## Supposé

- On cherche quand le membre envoie le formulaire, pas à chaque lettre tapée.

## Pas encore

- Chercher dans les notes des autres membres : hors de l'idée.
- Un historique des recherches : personne ne l'a demandé, et il garderait ce que les membres cherchent.

## Vérifs

- [x] Chaque récit nomme une personne de `idee.md` et pourquoi ça compte pour elle ? (US1, US2)
- [x] Chaque scénario se vérifie par quelqu'un qui ne code pas, en faisant et en regardant ? (US1, US2)
- [x] Chaque décision de `decisions.md` apparaît dans un récit ou sous Pas encore ? (US1)
- [x] Qui peut voir, changer ou télécharger chaque donnée personnelle est dit ? (US1, US2)
- [x] Chaque point ouvert est tranché, supposé, ou posé dans `a-trancher.md` avec un conseil ? (US1)
