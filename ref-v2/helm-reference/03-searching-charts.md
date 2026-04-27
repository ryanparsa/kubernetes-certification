# Helm Reference

[← Back to index](../README.md)

---

## 3. Searching Charts

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
