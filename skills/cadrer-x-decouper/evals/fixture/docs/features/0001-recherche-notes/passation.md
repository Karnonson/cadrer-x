# Recherche dans les notes — passation

## Maquette

- Lien : aucun — maquette locale : ouvrir maquette/recherche.html
- Style : docs/design-system
- La barre des états (`nav.maquette-etats`) et `maquette.js` sont propres à la maquette, jamais du code produit.

## Écrans

### SC1 Recherche

- Récits : US1
- Fichier : maquette/recherche.html
- Parties : nav, page, field (label, input), btn-primary, row, list, card (card-title, card-meta), empty, alert-error ; nouvelles : Surlignage
- États : avant (#avant) — l'invitation à taper un mot ; resultats (#resultats) — le compte, puis une carte par note, la plus récente d'abord : le livre, la page s'il y en a une, les mots autour avec le mot marqué, la date ; aucun (#aucun) — aucune note ne contient le mot, avec le mot tapé ; erreur (#erreur) — la recherche a échoué, le mot reste dans le champ
- Largeurs : 390 — le champ et le bouton l'un sous l'autre, les cartes sur toute la largeur ; 1280 — la page reste à 720 px, centrée, le champ et le bouton sur une ligne
- Contenu : contenu.md → SC1

### SC2 Note

- Récits : US2
- Fichier : maquette/note.html
- Parties : nav, page, back, card-meta ; nouvelles : aucune
- États : note (#note) — la note entière, son livre en titre, la page si elle est notée et la date, le lien de retour aux résultats
- Largeurs : 390 — une colonne ; 1280 — la page reste à 720 px, centrée
- Contenu : contenu.md → SC2

## Nouveautés

- Surlignage — le mot cherché marqué dans les mots autour, sur SC1 (`mark` dans `.snippet`). Le design system n'a pas de texte marqué ; fait avec `--color-accent-soft` et `--radius-sm`.

## Accessibilité

- SC1 : le champ a son libellé visible « Un mot de ta note » ; le compte des résultats est annoncé (`aria-live="polite"`) ; l'erreur aussi (`role="alert"`) ; chaque carte est un lien entier, d'au moins `--tap` de haut.
- SC2 : le lien de retour vient en premier dans l'ordre du focus.

## Ouvert

- aucun

## Contrôle

- [x] Chaque récit qu'une personne voit a son écran, et chaque scénario se fait sur un écran, dans un état.
- [x] Chaque `class` des pages est une partie du design system, une Nouveauté, ou la barre des états ; aucune couleur ni taille brute.
- [x] Chaque écran montre le moins de données personnelles possible, jamais celles d'un autre.
- [x] Un écran qui recueille des données dit pourquoi, et demande le consentement (jamais pré-coché) quand c'est sa base.
- [x] Chaque texte est dans `contenu.md`, tel que les pages le montrent ; un nombre qui varie a chaque forme.
- [x] Chaque champ a un libellé visible ; une erreur est annoncée (`role="alert"`), un résultat qui arrive aussi (`aria-live="polite"`) ; une cible tactile fait au moins la taille du design system.
- [x] Chaque page a été vue à 390 et à 1280, sans défilement de côté à 390 ; sinon, dit sous Ouvert.
