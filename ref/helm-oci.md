# Working with OCI Registries

Helm 3.8+ supports OCI registries (no `helm repo add` required).

```bash
# Pull from OCI registry
helm pull oci://registry.example.com/charts/my-chart --version 1.0.0

# Install directly from OCI registry
helm install my-release oci://registry.example.com/charts/my-chart \
  --version 1.0.0

# Push a chart to OCI registry
helm push my-chart-1.0.0.tgz oci://registry.example.com/charts
```

---

