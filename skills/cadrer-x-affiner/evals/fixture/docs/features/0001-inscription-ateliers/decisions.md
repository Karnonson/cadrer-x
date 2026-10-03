# Inscription aux ateliers — décisions
## Décisions
- D1 Les inscriptions ont leur propre module, `signup`, à côté des ateliers et des membres — pourquoi : il possède les inscriptions et la règle des places.
- D2 Un membre annule sa propre inscription jusqu'à 24 heures avant l'atelier ; après, il appelle Lise — pourquoi : les animateurs ont besoin d'un jour pour redonner la place à la main.
- D3 Les animateurs téléchargent la liste d'un atelier dans un fichier que leur tableur ouvre — pourquoi : Lise l'imprime pour l'accueil.
## Étapes
- écrans : oui
- code : oui
- données : oui
## Précisions
- Q : Un membre peut-il s'inscrire deux fois au même atelier ? → R : Non : une place par membre et par atelier.
- Q : Que voit un membre quand un atelier est complet ? → R : Qu'il est complet ; il n'y a pas de liste d'attente.
## Stack
aucun
## Impact archi
Un nouveau module `signup` et une nouvelle table des inscriptions (quel membre, quel atelier, quand, annulée ou non) : les premières données personnelles gardées hors du module des membres.
## Données et risques
- Données personnelles : quel membre s'est inscrit à quel atelier, et quand. Base : l'intérêt légitime du club à organiser ses ateliers. Durée : effacées 12 mois après l'atelier.
- La liste téléchargée contient des noms et des e-mails : animateurs seulement, et le fichier n'est jamais gardé sur le serveur.
- Abus : un membre qui annule l'inscription d'un autre ; deux inscriptions en même temps pour la dernière place ; un membre qui n'est pas animateur et télécharge la liste.
## À faire
aucun
