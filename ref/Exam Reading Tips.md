# Exam Reading Tips

## The Problem
Under pressure, your brain pattern-matches familiar words and skips unfamiliar ones.
Example: reading "Find the Issue" instead of "Find the **Issuer**".

## Before Starting a Question

- **Read the last sentence first** — that's usually the actual task. Then read the full question for context.
- Read the question **twice** before touching the terminal.

## While Reading

- Point at each word with your cursor as you read — forces your eye to land on each word individually.
- Say the key nouns in your head: *"Find... the... Issuer"*.

## The Task Line Habit

Copy-paste the exact task into your terminal as a comment before starting:

```bash
# TASK: Find the Issuer of the cert in namespace foo
```

This forces you to type it out and catches misreads immediately.

## Common Kubernetes Misread Traps

These word pairs are visually similar and frequently confused under exam pressure:

| Easy to misread as | Actually says |
|--------------------|---------------|
| `Issue` | `Issuer` |
| `Role` | `RoleBinding` |
| `ClusterRole` | `ClusterRoleBinding` |
| `ServiceAccount` | `Service` |
| `Deployment` | `DaemonSet` |
| `configmap` | `secret` |
| namespace `default` | namespace `kube-system` (or a custom one) |

## Watch for Negative Constraints

Questions often include hard constraints that are easy to miss:

- **"Do NOT delete"** — the checker will fail if you recreate the resource
- **"Do NOT restart"** — edit in-place; avoid delete+recreate
- **"Must not change"** — a field is off-limits even if it would make your life easier
- **"existing … must continue to work"** — your change must be backward-compatible

Scan for `not`, `must not`, `do not`, `without`, and `existing` before you start typing.

## Namespace and Context Are Part of the Answer

Questions that specify a namespace or cluster context are testing whether you read them.

- Note the **exact namespace** before opening the terminal — `kube-system` ≠ `kube-public` ≠ `default`.
- Note the **exact resource name** — `web` ≠ `webapp` ≠ `web-app`.
- If the question says "on cluster `k8s`", switch context first (see [Exam Strategy](Exam%20Strategy.md)).

## During the Exam

- The real CKA lets you flag questions and return.
- If something feels off ("why can't I find any Issues?"), **stop and re-read the question from scratch** — you likely misread a key word.
