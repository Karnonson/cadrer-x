# cadrer-x — feuille de route

## Pour la v2

0. Corriger ce que les essais de la v1 ont montré, dans l'ordre de leur verdict.

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
- Les compétences ne dictent plus les mots que l'agent dit à la personne. Aujourd'hui des phrases
  en français sont écrites en dur dans leurs consignes (« Ces détails : on les corrige maintenant,
  ou on livre tel quel ? », « tel quel »…). La règle à appliquer : une compétence donne l'intention
  d'un message et ce que la réponse décide ; le modèle le formule dans la langue de la personne ;
  seuls les libellés, les ids et les noms de fichiers de `docs/conventions.md` restent des chaînes
  fixes. Même question côté réponses : les mots qui valent un oui ou une hésitation (« oui »,
  « ok », « ça va », « c'est bon », « bof », « comme tu veux » ; `cadrer-x-choisir/SKILL.md:101-108`,
  `cadrer-x-init/SKILL.md:58-60`, `cadrer-x-ranger/SKILL.md:69`, `references/spec.md:18`,
  `references/decoupe.md:137`, `docs/conventions.md:74`) supposent aussi le français. Les endroits
  à reprendre (hors prompts des sous-agents, qui s'adressent à un modèle, et hors contenu des
  fichiers) :
  - `skills/cadrer-x-realiser/SKILL.md:112-113` et `:118` : la question sur les détails,
    « tel quel », « Maintenant » ;
  - `skills/cadrer-x-choisir/SKILL.md:49` : « Qu'est-ce que tu veux changer ? » ;
  - `skills/cadrer-x-choisir/SKILL.md:102` : « Si tu n'avais pas à le justifier, tu voudrais
    quoi ? » ;
  - `skills/cadrer-x-choisir/SKILL.md:134` et `skills/cadrer-x-init/SKILL.md:79` : le format
    « ➡️ Mon idée : … — confiance ~40 % (il manque : …) » ;
  - `skills/cadrer-x-choisir/SKILL.md:193` : « Reste 4 décisions, je commence. » ;
  - `skills/cadrer-x-choisir/SKILL.md:210` : « Petit changement : je prends la voie courte. » ;
  - `skills/cadrer-x-choisir/SKILL.md:228` et `skills/cadrer-x-choisir/references/spec.md:92` : le
    format « ➡️ Conseil : A — … « Oui » le prend ; ou une lettre, ou tes mots. » ;
  - `skills/cadrer-x-choisir/SKILL.md:341-342` : « Ces mots et ce look : c'est bon ? » ;
  - `skills/cadrer-x-init/SKILL.md:110` : « continuer, ou passer à X ? » ;
  - à la limite : `skills/cadrer-x-rendre/SKILL.md:79`, « tu l'as choisi », écrit dans l'ADR, pas
    dit.

## Idées en attente

- Des techniques de remue-méninges dans `choisir` : SCAMPER, le remue-méninges inversé, lever une
  contrainte, et trois autres méthodes structurées, avec une protection contre les biais.
- Reconnaître seul un projet existant et en écrire l'analyse avant le premier entretien.
