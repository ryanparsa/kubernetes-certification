# Helm Reference — 3. Searching Charts

> Part of [Helm Reference](../Helm Reference.md)


```bash
# Search all configured repos for a chart
helm search repo <keyword>
helm search repo minio

# Search with version info
helm search repo nginx --versions

# Search Artifact Hub (public registry — requires internet)
helm search hub <keyword>

# Show all available chart versions
helm search repo bitnami/nginx --versions
```

---

