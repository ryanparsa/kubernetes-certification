# Uninstalling a Release

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

