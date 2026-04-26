# Prompts

Modular prompts for Kubernetes certification exam practice. Combine them by pasting multiple files into a single AI session.

Each exam scope prompt (`cka.md`, `ckad.md`, etc.) is a thin wrapper — it lists the domain weights and links to the canonical exam definition in the corresponding exam directory (e.g., `cka/README.md`). All topic details live in those files.

## Files

| File | Type | Description |
|---|---|---|
| `base.md` | Base | Shared rules: format, grading, difficulty ramp. Always include. |
| `cka.md` | Exam scope | CKA domains → see [cka/README.md](../cka/README.md) |
| `ckad.md` | Exam scope | CKAD domains → see [ckad/README.md](../ckad/README.md) |
| `cks.md` | Exam scope | CKS domains → see [cks/README.md](../cks/README.md) |
| `kcsa.md` | Exam scope | KCSA domains → see [kcsa/README.md](../kcsa/README.md) |
| `docs.md` | Practice type | Docs navigation drills. Standalone — no base needed. |
| `troubleshoot.md` | Practice type | Symptoms-only challenges. Diagnose root cause and fix. |
| `speed.md` | Practice type | Imperative commands only. No writing YAML from scratch. |
| `yaml.md` | Practice type | Write complete manifests from scratch. Inline error annotation. |
| `mock.md` | Practice type | Full timed exam. All tasks at once, multiple contexts, scored out of 100. |

## Usage

Paste the contents of each file into your session in order: base → exam scope → practice type.

| Goal | Prompts |
|---|---|
| General CKA drill | `base` + `cka` |
| General CKAD drill | `base` + `ckad` |
| General CKS drill | `base` + `cks` |
| General KCSA drill | `base` + `kcsa` |
| CKA troubleshooting | `base` + `cka` + `troubleshoot` |
| CKAD troubleshooting | `base` + `ckad` + `troubleshoot` |
| CKAD speed practice | `base` + `ckad` + `speed` |
| CKA speed practice | `base` + `cka` + `speed` |
| YAML muscle memory (either exam) | `base` + `cka` or `ckad` + `yaml` |
| Docs navigation | `docs` (standalone) |
| Full mock exam | `base` + `cka` or `ckad` + `mock` |
