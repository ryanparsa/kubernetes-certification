# Helm Reference

[← Back to index](../README.md)

---

## 11. Downloading and Packaging Charts

```bash
# Download a chart tarball to current directory
helm pull bitnami/nginx
# → nginx-15.1.0.tgz

# Download and extract
helm pull bitnami/nginx --untar

# Download a specific version
helm pull bitnami/nginx --version 15.0.0

# Create a new chart scaffold
helm create my-chart
# → my-chart/
#     Chart.yaml
#     values.yaml
#     templates/

# Package a local chart directory into a tarball
helm package ./my-chart/
```

---
