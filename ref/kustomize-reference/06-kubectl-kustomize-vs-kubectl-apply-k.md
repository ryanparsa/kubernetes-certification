# Kustomize Reference — 6. `kubectl kustomize` vs `kubectl apply -k`

> Part of [Kustomize Reference](../Kustomize Reference.md)


| Command | Effect |
|---|---|
| `kubectl kustomize <dir>` | Build and print YAML to stdout — does NOT apply to cluster |
| `kubectl apply -k <dir>` | Build and apply to cluster in one step |
| `kubectl kustomize <dir> \| kubectl apply -f -` | Equivalent to `apply -k` but allows `--dry-run` or `diff` in between |
| `kubectl kustomize <dir> \| kubectl diff -f -` | Preview what would change |
| `kubectl delete -k <dir>` | Delete all resources in the built YAML |

```bash
# Preview what would be applied
kubectl kustomize staging | kubectl diff -f -

# Apply staging overlay
kubectl kustomize staging | kubectl apply -f -
# or
kubectl apply -k staging

# Apply prod overlay
kubectl apply -k prod

# Check the built output before applying
kubectl kustomize prod | less

# Apply and watch rollout
kubectl apply -k prod && kubectl rollout status deployment/api-gateway -n api-gateway-prod
```

---

