# Kubernetes RBAC Reference

[← Back to index](../README.md)

---

## 10. Quick Reference

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
