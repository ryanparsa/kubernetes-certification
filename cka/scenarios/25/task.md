# Task 25 — Networking: Egress NetworkPolicy

**Context:** Cluster `cka-task-25` (`export KUBECONFIG=$PWD/kubeconfig`)

Namespace `restricted` contains pods labeled `tier=frontend`.

## Objective

Create a **NetworkPolicy** named **`restrict-egress`** in the **`restricted`** namespace that:

1. Applies only to pods with label **`tier=frontend`**.
2. Allows **egress** traffic to any pod in the **`external-world`** namespace
   only on **TCP port 5432**.
3. Allows **egress** traffic to any destination on **UDP port 53** (DNS resolution).
4. Denies all other egress traffic (this is implied if egress rules are present).

The grader checks the resource structure.

## Verify

```
./test.sh
```
