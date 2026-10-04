# cadrer-x — vision

## Vision

Anyone with an idea for software can build it, ship it and keep it dependable, without becoming a
developer.

## Pour qui

People who don't code and have an idea for software, for themselves, their work or a small business.
They use a coding agent (Claude Code or codex) to build it, and pay for it themselves. They don't know
the software development life cycle or its best practices. Today they prompt the agent directly.

## Besoins

A coding agent writes code fast, but leaves the person every decision that keeps software alive: what
exactly to build, how to test it, whether it is safe, how to put it online and take it back. Without
that knowledge they get software that works in the demo, then breaks, leaks or can't be changed. They
need the agents to carry that work and ask them only what is theirs to decide, the product. A small
change must not go through the whole process.

Last real case: to fill in.

## Produit

- One step at a time, from the idea to the release: each step writes a file the next one reads, so
  nothing is decided twice or lost on the way.
- The person decides only the product, in plain words; technical facts are looked up, never asked.
- Every story is reviewed by an agent that did not build it, and nothing is merged or put online
  without the person's yes.
- Modules, tests and the project's rules from the first feature, so the software stays safe and
  changeable as it grows.
- A short path for small changes.

## Objectifs

1. An engaged francophone audience: people who use cadrer-x on a project of their own and come back
   for the next one. Number and date: to set.
2. A non-coder takes a feature from the idea to the release without touching code or making a
   technical decision. Number and date: to set.
3. A small change or a bug stays quick. Number and date: to set.

## Faire ou louer

Faire. The repeatable path itself exists elsewhere; what is missing is that path for someone who
doesn't code, in French (checked in October 2026):

- Workflows for coding agents that reach the release: gstack (garrytan/gstack) runs from "is this
  worth building" to a deploy with a revert and a check after it; GSD (open-gsd/gsd-core) has a mode
  that rewords its questions for a non-technical owner. Both are in English and ask technical
  questions; gstack is a menu of commands, GSD stops at the pull request.
- Spec-driven workflows (GitHub Spec Kit, BMAD Method, OpenSpec, Superpowers, Kiro): repeatable, for
  developers; most stop at the merge.
- App builders (Lovable, Replit, Bolt): made for non-coders, with some guards (a security scan before
  publishing, going back to a checkpoint), but the work is prompt after prompt: no written decisions,
  no review by someone who did not build it, tied to their platform.
- Skill packs for non-technical founders (solo-founder-skills, vibe-check): advice and checklists for
  each stage, not steps that hand their work to the next one.

What every option lacks: one path, in French, from the idea to the release, where the person is never
asked a technical question and nothing ships without their yes. That gap is narrow and easy to copy:
the audience and the community around it are what keeps it.
