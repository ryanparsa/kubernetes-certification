# Helm Reference

[← Back to index](../README.md)

---

## 10. Templating

`helm template` renders chart templates locally without contacting the cluster. Useful for
inspecting what will be applied or for piping into `kubectl apply`.

```bash
# Render all templates to stdout
helm template <release-name> <chart>
helm template my-nginx bitnami/nginx

# Render with custom values
helm template my-nginx bitnami/nginx \
  --set replicaCount=3 \
  -f custom-values.yaml

# Render to a file
helm template my-nginx bitnami/nginx > rendered.yaml

# Pipe directly to kubectl (GitOps-style)
helm template my-nginx bitnami/nginx | kubectl apply -f -

# Render only specific templates
helm template my-nginx bitnami/nginx \
  --show-only templates/deployment.yaml
```

---
