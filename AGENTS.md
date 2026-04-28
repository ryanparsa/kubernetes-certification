# AGENTS

This file provides instructions for LLMs (AI coding agents) working in this repository.

## Memory

Use the `.memory/` directory to store and read persistent memory across sessions.

- Each category has its own file (e.g. `.memory/cka.md`, `.memory/kcna.md`, `.memory/conventions.md`, `.memory/ci.md`).
- Add one fact per line - keep each line concise and self-contained so any LLM can learn it at a glance.
- Read all files in `.memory/` at the start of every session to load prior context.
- Append new discoveries, patterns, or gotchas to the appropriate category file as you work.

## Repository Layout

| Path | Contents |
|------|----------|
| `cka/` | CKA practice labs, numbered sequentially (`cka/<N>/`) |
| `kcna/` | KCNA study material (no lab structure) |
| `cka/ref/` | Verbatim killer.sh simulator sources (`a.md`, `b.md`) |
| `.memory/` | LLM persistent memory (one file per category) |
| `CONTRIBUTING.md` | Full lab structure, file templates, and conventions |

## Key Rules

- `cka/29/` is the canonical reference lab - use it as a template.
- Never paraphrase or reformat `readme.md` files; content must match `cka/ref/` verbatim.
- `fix.sh` must be idempotent (`kubectl apply`, not `kubectl create`).
- `kubeconfig.yaml` and `lab/` are git-ignored - never commit them.
- Every lab needs a CI workflow at `.github/workflows/<exam>-lab-<N>.yml` using `helm/kind-action@v1`.
