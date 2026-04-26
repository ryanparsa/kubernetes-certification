# Prompts

Modular prompts for CKA and CKAD exam practice. Combine them by pasting multiple files into a single AI session.

## Files

| File | Type | Description |
|---|---|---|
| `base.md` | Base | Shared rules: format, grading, difficulty ramp. Always include. |
| `cka.md` | Exam scope | CKA-specific topics: kubeadm, etcd, certs, node/control-plane troubleshooting. |
| `ckad.md` | Exam scope | CKAD-specific topics: multi-container patterns, Helm, CRDs, deployment strategies. |
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
| CKA troubleshooting | `base` + `cka` + `troubleshoot` |
| CKAD speed practice | `base` + `ckad` + `speed` |
| YAML muscle memory (either exam) | `base` + `cka` or `ckad` + `yaml` |
| Docs navigation | `docs` (standalone) |
| Full mock exam | `base` + `cka` or `ckad` + `mock` |
