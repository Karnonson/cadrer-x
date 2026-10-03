<!--
  Modèle de passation.md cadrer-x. Trois lecteurs : la personne, qui regarde la maquette ; `découper`,
  qui donne à chaque tâche ses écrans (`Écrans : SC1`) ; et celui qui construit une tâche, qui cite la
  section de son écran mot pour mot et construit à partir d'elle et de la maquette seules.
  Titres, libellés et identifiants tels quels ; le texte dans la langue de la personne. Une section
  vide dit `aucun`. Chaque ligne d'un écran tient sur une ligne. Retirer ces commentaires.
-->

# <Titre> — passation

## Maquette

- Lien : <adresse Claude Design (https://…), ou `aucun — maquette locale` : ouvrir maquette/<page>.html>
- Style : <le chemin du design system, ou `maquette/styles.css, neutre : pas encore de design system`>
- La barre des états (`nav.maquette-etats`) et `maquette.js` sont propres à la maquette, jamais du code produit.

## Écrans

### SC1 <nom court>

- Récits : US1, US3
- Fichier : maquette/<page>.html
- Parties : <les parties du design system, par leurs noms> ; nouvelles : <chaque Nouveauté utilisée, ou aucune>
- États : <état> (#<ancre>) — <ce qu'on voit> ; <état> (#<ancre>) — <ce qu'on voit>
- Largeurs : 390 — <ce qui change> ; 1280 — <ce qui change>
- Textes : textes.md → SC1

## Nouveautés

- <Nom> — <ce que c'est, où ça se voit>. <pourquoi aucune partie du design system ne le fait> ; fait avec <tokens>.

## Accessibilité

- SC1 : <les libellés, l'ordre du focus, ce qu'entend un lecteur d'écran, le contraste de ce qui est nouveau>

## Ouvert

- aucun

## Contrôle

<!-- Vérifié sur les pages elles-mêmes (leur HTML), pas de mémoire. Une case qui échoue change la maquette ou ce fichier. -->

- [ ] Chaque récit qu'une personne voit a son écran, et chaque scénario se fait sur un écran, dans un état.
- [ ] Chaque `class` des pages est une partie du design system, une Nouveauté, ou la barre des états ; aucune couleur ni taille brute.
- [ ] Chaque écran montre le moins de données personnelles possible, jamais celles d'un autre.
- [ ] Un écran qui recueille des données dit pourquoi, et demande le consentement (jamais pré-coché) quand c'est sa base.
- [ ] Chaque texte est dans `textes.md`, tel que les pages le montrent ; un nombre qui varie a chaque forme.
- [ ] Chaque champ a un libellé visible ; une erreur est annoncée (`role="alert"`), un résultat qui arrive aussi (`aria-live="polite"`) ; une cible tactile fait au moins la taille du design system.
- [ ] Chaque page a été vue à 390 et à 1280, sans défilement de côté à 390 ; sinon, dit sous Ouvert.
