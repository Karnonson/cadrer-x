# Carnet — architecture

## Pièces

- L'appli web, que les membres ouvrent dans leur navigateur, sur Cloud Run — Next.js 15 (App Router), TypeScript
- La base, qui garde les membres, les livres et les notes — Turso (libSQL)
- La connexion par lien reçu par e-mail — Better Auth

## Modules

| Module | Possède | Chemins |
|---|---|---|
| accounts | les membres, les sessions, les réglages | `src/modules/accounts/{ui,server,data}` |
| notes | les livres et les notes ; appelle accounts | `src/modules/notes/{ui,server,data}` |
| shared-db | la connexion à Turso | `src/modules/shared-db/` |
| shared UI | les parties du design system en code (Button, Field, Card, Alert), les tokens de l'appli | `src/components/`, `src/styles/tokens.css` |

Les pages de `src/app/` restent minces : elles appellent le `server/` d'un module et affichent son `ui/`.
Un `ui/` n'interroge jamais la base. Un module n'en utilise un autre que par son `server/index.ts`.

## Données

Turso : les membres (e-mail, nom affiché), les sessions, les livres, les notes (le texte écrit par le
membre, le livre, la page). Chaque membre ne voit que ses notes. Copie quotidienne de Turso.

## Secrets

`TURSO_DATABASE_URL`, `TURSO_AUTH_TOKEN`, `BETTER_AUTH_SECRET` : dans les réglages de Cloud Run, `.env.local` en local, jamais dans le dépôt.

## Coût

Cloud Run et Turso dans leurs offres gratuites à l'usage actuel.

## En local

`pnpm dev` avec une base Turso locale (`turso dev`).

## Lancer

Les commandes de `cadrer-x.yml` : `pnpm lint`, `pnpm exec tsc --noEmit`, `pnpm test` (vitest et Testing Library).

## Trajet

Tu ouvres tes notes → l'appli vérifie ta session → elle lit tes notes dans Turso → tu les vois, la plus récente d'abord.

## À faire

aucun

## Écarté

- Une recherche hébergée (Algolia) : un service de plus, et les notes des membres chez un tiers.

## Mots

- Membre : jamais « utilisateur » à l'écran.
- Note : ce qu'un membre écrit sur un livre.
- Livre, étagère.
