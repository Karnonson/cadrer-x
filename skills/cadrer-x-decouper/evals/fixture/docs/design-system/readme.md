# Carnet — design system

The one source of Carnet's look. `styles.css` holds every token and every part; `index.html` shows
them. In the app, the tokens are `src/styles/tokens.css` (short names of its own, from before this
system) and the parts are the React components of `src/components/` (Button, Field, Card, Alert).

## Tokens
Colours `--color-*`, fonts `--font-body` (reading) and `--font-ui` (controls), sizes `--text-*`,
spaces `--space-*`, `--radius-*`, `--shadow-sm`, and `--tap` (44 px, the smallest thing a finger taps).

## Parts
| Part | Classes | In the app |
|---|---|---|
| Page | `.page` | the layout |
| Nav bar | `.nav`, `.nav-brand`, `.nav-meta` | the layout |
| Button | `.btn` + `.btn-primary` / `.btn-ghost` | `Button` |
| Field | `.field`, `.label`, `.input`, `.field-hint`, `.field-error` | `Field` |
| Card | `.card`, `.card-title`, `.card-meta` | `Card` |
| Alert | `.alert` + `.alert-error` / `.alert-info` | `Alert` |
| Empty message | `.empty` | — |
| List | `.list` | — |
| Row | `.row` | — |
| Back link | `.back` | — |

## Rules
- Never a raw colour, size or font outside this file: a token.
- A part this system lacks is built from tokens in the feature that needs it, and listed in its
  handoff.md with why. The system's owner decides whether it joins here; a feature never edits this folder.
- Text passes WCAG AA; every control shows a focus ring; nothing a finger taps is under `--tap`.
