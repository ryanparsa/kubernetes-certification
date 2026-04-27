# Helm Reference — 6. Listing and Inspecting Releases

> Part of [Helm Reference](../Helm Reference.md)


```bash
# List all releases in current namespace
helm list
helm ls

# List releases in a specific namespace
helm list -n kube-system
helm ls -n minio

# List releases in all namespaces
helm list -A
helm ls -A

# Show a release's status and metadata
helm status <release-name> -n <namespace>
helm status my-nginx -n ingress

# Show the computed values used by a release
helm get values my-nginx -n ingress

# Show the values including defaults
helm get values my-nginx -n ingress --all

# Show the rendered manifests for a release
helm get manifest my-nginx -n ingress

# Show the chart notes
helm get notes my-nginx -n ingress
```

---

