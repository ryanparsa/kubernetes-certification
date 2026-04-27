# Helm Reference — 4. Inspecting a Chart Before Installing

> Part of [Helm Reference](../Helm Reference.md)


```bash
# Show chart metadata (description, version, app version)
helm show chart bitnami/nginx

# Show the default values.yaml for a chart
helm show values bitnami/nginx

# Show the README
helm show readme bitnami/nginx

# Show everything (chart + values + readme)
helm show all bitnami/nginx
```

---

