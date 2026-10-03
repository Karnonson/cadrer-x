# Inscription aux ateliers — spec

**Branche** : `feature/inscription-ateliers`
**Créée** : 2026-10-02
**Statut** : validée
**Source** : `idee.md`, `decisions.md`

## Récits

### US1 — S'inscrire à un atelier (Priorité : P1)

En tant que membre, je veux m'inscrire à un atelier qui a une place libre afin d'avoir ma place sans écrire à Lise.

**Pourquoi cette priorité** : c'est le Résultat de l'idée.

**Test seul** : se vérifie en s'inscrivant à un atelier avec des places, puis à un atelier complet.

**Scénarios** :

1. **Étant donné** un atelier avec une place libre, **quand** je m'inscris, **alors** j'ai une place, et l'atelier a une place libre de moins.
2. **Étant donné** un atelier complet, **quand** je veux m'inscrire, **alors** on me dit qu'il est complet, et je ne suis pas inscrit.
3. **Étant donné** que je suis déjà inscrit, **quand** je m'inscris encore, **alors** j'ai toujours une seule place.

---

### US2 — Annuler mon inscription (Priorité : P2)

En tant que membre, je veux annuler mon inscription jusqu'à 24 heures avant l'atelier afin que quelqu'un d'autre prenne ma place.

**Pourquoi cette priorité** : une place rendue sert un autre membre.

**Test seul** : se vérifie en annulant une inscription trois jours avant, puis la veille.

**Scénarios** :

1. **Étant donné** un atelier dans plus de 24 heures, **quand** j'annule, **alors** ma place redevient libre.
2. **Étant donné** un atelier dans moins de 24 heures, **quand** j'annule, **alors** on me dit d'appeler Lise, et ma place reste à moi.
3. **Étant donné** l'inscription d'un autre membre, **quand** j'essaie de l'annuler, **alors** on me le refuse.

---

### US3 — Voir qui vient (Priorité : P3)

En tant qu'animateur, je veux la liste des inscrits d'un atelier afin de savoir qui vient sans tableur.

**Pourquoi cette priorité** : c'est l'autre moitié du Résultat.

**Test seul** : se vérifie en demandant la liste d'un atelier qui a des inscrits.

**Scénarios** :

1. **Étant donné** un atelier avec des inscrits, **quand** je demande la liste, **alors** je vois le nom et l'e-mail de chacun, le premier inscrit d'abord, sans les annulés.
2. **Étant donné** un membre qui n'est pas animateur, **quand** il demande la liste, **alors** on la lui refuse.

### Cas limites

- Deux membres pour la dernière place au même moment : un seul l'obtient.

## Exigences

- **EF1** : L'appli NE DOIT JAMAIS compter plus d'inscrits que de places.
- **EF2** : Un membre DOIT avoir au plus une place par atelier.
- **EF3** : Un membre DOIT pouvoir annuler sa propre inscription jusqu'à 24 heures avant le début, et plus après.
- **EF4** : Seuls les animateurs DOIVENT voir la liste des inscrits.

### Données clés

- **Inscription** : quel membre, quel atelier, quand, annulée ou non. Effacée 12 mois après l'atelier.

## Critères

- **CS1** : D'ici le 30 novembre, au moins 80 % des inscriptions d'automne faites par les membres eux-mêmes.
- **CS2** : Aucun atelier d'automne avec plus d'inscrits que de places.

## Supposé

- La limite des 24 heures se compte depuis l'heure de début de l'atelier.

## Pas encore

- Inscrire quelqu'un sans compte : Q1, tranchée non.
- Le téléchargement de la liste : sa propre fonctionnalité, après celle-ci.
- Les listes d'attente, les rappels, le paiement : hors de l'idée.

## Vérifs

- [x] Chaque récit nomme une personne de `idee.md` et pourquoi ça compte pour elle ? (US1, US2, US3)
- [x] Chaque scénario se vérifie par quelqu'un qui ne code pas, en faisant et en regardant ? (US1, US2, US3)
- [x] Chaque décision de `decisions.md` apparaît dans un récit ou sous Pas encore ? (US1, US2, US3)
- [x] Qui peut voir, changer ou télécharger chaque donnée personnelle est dit ? (US2, US3)
- [x] Chaque point ouvert est tranché, supposé, ou posé dans `a-trancher.md` avec un conseil ? (US1)
