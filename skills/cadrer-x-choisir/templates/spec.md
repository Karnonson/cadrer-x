<!--
  Modèle de spec cadrer-x, adapté du modèle de spec de spec-kit
  (https://github.com/github/spec-kit/blob/main/templates/spec-template.md, licence MIT, © GitHub, Inc.).
  Les titres, libellés et identifiants restent tels quels, dans toutes les langues : les étapes
  suivantes les cherchent par ces noms. Le texte sous les titres est dans la langue de la personne.
  Retirer ces commentaires dans la spec écrite.
-->

# <Titre> — spec

**Branche** : `feature/<slug>`
**Créée** : <AAAA-MM-JJ>
**Statut** : brouillon
**Source** : `brief.md`, `decisions.md`

## Récits

<!--
  Classés par importance. Chaque récit se teste seul : développé seul, il apporte déjà quelque chose
  qu'on peut montrer. P1 est le plus important ; `bonus` : voulu seulement s'il reste du temps,
  développé après les autres.
-->

### US1 — <titre court> (Priorité : P1)

En tant que <qui, tiré de brief.md>, je veux <quoi> afin de <pourquoi>.

**Pourquoi cette priorité** : <la valeur, et pourquoi ce rang>

**Test seul** : <comment le vérifier seul — « se vérifie entièrement en <action> et apporte <valeur> »>

**Scénarios** :

1. **Étant donné** <l'état de départ>, **quand** <l'action>, **alors** <ce qu'on voit>
2. **Étant donné** <l'état de départ>, **quand** <l'action>, **alors** <ce qu'on voit>

---

### US2 — <titre court> (Priorité : P2)

En tant que <qui>, je veux <quoi> afin de <pourquoi>.

**Pourquoi cette priorité** : <…>

**Test seul** : <…>

**Scénarios** :

1. **Étant donné** <…>, **quand** <…>, **alors** <…>

---

<!-- Autant de récits que nécessaire, chacun avec sa priorité. -->

### Cas limites

<!-- Les cas gênants : plein, deux fois, trop tard, les données de quelqu'un d'autre, une erreur à défaire. -->

- Que se passe-t-il quand <limite> ?
- Que fait l'appli quand <erreur> ?

## Exigences

<!--
  Ce que l'appli DOIT faire, vérifiable sans lire le code. Chaque tâche de `taches.md` liste les
  exigences qu'elle porte (`Exigences : EF1, EF3`). Un point pas encore tranché : marqué ici,
  et sa question dans `a-trancher.md`.
-->

- **EF1** : L'appli DOIT <capacité précise>
- **EF2** : Les <qui> DOIVENT pouvoir <action clé>
- **EF3** : L'appli DOIT garder <données> pendant [À PRÉCISER : durée non décidée → Q1]

### Données clés

<!-- Si la fonctionnalité garde des données : ce que chaque chose représente, sans parler de technique. -->

- **<Chose 1>** : <ce qu'elle représente, ce qu'on en garde>
- **<Chose 2>** : <ce qu'elle représente, à quoi elle est liée>

## Critères

<!-- Mesurables, sans technique, tirés de la Mesure de brief.md. -->

- **CS1** : <« un client réserve un appel en moins de 2 minutes »>
- **CS2** : <« moins d'1 appel manqué sur 10 d'ici le 31 janvier »>

## Supposé

<!-- Ce que la spec a choisi seule, faute de précision : des choix par défaut que personne ne contesterait. -->

- <supposition sur les personnes, le périmètre, les données ou un service existant>

## Pas encore

<!-- Ce qui reste hors de cette version, et ce qui le ferait revenir. -->

- <…>

## Vérifs

<!-- Des questions oui/non sur la façon dont la spec est écrite, suivies des récits qu'elles couvrent. -->

- [ ] Chaque récit nomme une personne de `brief.md` et pourquoi ça compte pour elle ? (tous)
- [ ] Chaque scénario se vérifie par quelqu'un qui ne code pas, en faisant et en regardant ? (tous)
- [ ] Chaque décision de `decisions.md` apparaît dans un récit ou sous Pas encore ? (…)
- [ ] Qui peut voir, changer ou télécharger chaque donnée personnelle est dit ? (…)
- [ ] Chaque point ouvert est tranché, supposé, ou posé dans `a-trancher.md` avec un conseil ? (…)
