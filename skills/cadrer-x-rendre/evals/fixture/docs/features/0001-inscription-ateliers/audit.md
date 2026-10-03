# Inscription aux ateliers — audit

## US3 Voir qui vient

**Tour** : 1
**Date** : 2026-10-02
**Verdict** : validé

### Spec

- Info : le scénario 1 tient : `attendees.py:9` trie par heure d'inscription, sans les annulés ; `test_an_organizer_sees_each_name_and_email_first_come_first_without_the_cancelled` le prouve, et échoue quand on retire le filtre des annulés.
- Info : le scénario 2 tient : le rôle est vérifié par `members.is_organizer`, côté serveur.

### Règles

- Info : M3 et M6 tenues : la liste passe par l'api.py des membres, le rôle est vérifié avant toute lecture.

### Non jugé

Vérifs : lancées — `PYTHONPATH=src python3 -m unittest discover -s tests -q`, code de sortie 0, « Ran 18 tests … OK »
- aucun

## US2 Annuler mon inscription

**Tour** : 1
**Date** : 2026-10-02
**Verdict** : validé

### Spec

- Info : les trois scénarios tiennent, et la limite exacte des 24 heures est testée (`test_exactly_24_hours_before_is_still_allowed`).
- Détail : `cancel.py:22` lit l'heure de début telle qu'elle est gardée ; une heure sans décalage ferait planter la comparaison. Toutes les heures gardées sont en UTC aujourd'hui.

### Règles

- Info : une annulation d'un autre membre est refusée et ne change rien (`test_risk_another_members_sign_up_cannot_be_cancelled`).

### Non jugé

Vérifs : lancées — `PYTHONPATH=src python3 -m unittest discover -s tests -q`, code de sortie 0, « Ran 18 tests … OK »
- aucun

## US1 S'inscrire à un atelier

**Tour** : 2
**Date** : 2026-10-01
**Verdict** : validé

### Spec

- Corrigé : la dernière place était donnée deux fois (`taken > seats`) — `signup/api.py:40`, `>=`, prouvé par `test_a_full_workshop_refuses_the_sign_up` qui part d'un atelier d'une place.
- Corrigé : la course pour la dernière place — `signup/api.py:34`, `BEGIN IMMEDIATE`, prouvé par `test_risk_two_sign_ups_at_once_for_the_last_seat` avec deux connexions.

### Règles

- Corrigé : `_member_exists` lisait la table des membres — remplacé par `members.get_member` (`signup/api.py:32`).
- Corrigé : `my_sign_ups`, non demandé, retiré.

### Correctifs

- aucun

### Non jugé

Vérifs : lancées — `PYTHONPATH=src python3 -m unittest discover -s tests -q`, code de sortie 0, « Ran 18 tests … OK »
- aucun
