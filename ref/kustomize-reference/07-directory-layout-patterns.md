# Kustomize Reference — 7. Directory Layout Patterns

> Part of [Kustomize Reference](../Kustomize Reference.md)


### Base + multiple overlays

```
app/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── serviceaccount.yaml
├── staging/
│   ├── kustomization.yaml   # resources: [../base]; patches for staging
│   └── patch.yaml
└── prod/
    ├── kustomization.yaml   # resources: [../base]; patches for prod
    └── patch.yaml
```

### Overlay kustomization.yaml (minimal)

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../base

patches:
  - path: patch.yaml

transformers:
  - |-
    apiVersion: builtin
    kind: NamespaceTransformer
    metadata:
      name: notImportantHere
      namespace: api-gateway-staging
```

---

