# Kubernetes RBAC Reference — 10. Quick Reference

> Part of [Kubernetes RBAC Reference](../RBAC Reference.md)


| Subject format for `--as` | Example |
|---|---|
| User | `jane` |
| ServiceAccount | `system:serviceaccount:NAMESPACE:NAME` |
| Group | `system:masters` |

| `subjects[].kind` values in YAML | |
|---|---|
| `User` | Human user authenticated via kubeconfig |
| `Group` | Group of users (e.g. `system:authenticated`) |
| `ServiceAccount` | Pod identity; `namespace` field required |
