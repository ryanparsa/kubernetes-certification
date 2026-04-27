# Helm Reference — 9. Uninstalling a Release

> Part of [Helm Reference](../Helm Reference.md)


```bash
# Uninstall a release (removes all resources and the release secret)
helm uninstall <release-name>
helm uninstall my-nginx -n ingress

# Keep release history (can rollback/inspect after uninstall)
helm uninstall my-nginx -n ingress --keep-history

# Dry-run uninstall
helm uninstall my-nginx --dry-run
```

---

