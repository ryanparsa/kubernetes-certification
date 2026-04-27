# Kustomize Reference — 1. Core Concept

> Part of [Kustomize Reference](../Kustomize Reference.md)


Kustomize works on **overlays** layered on top of a **base**:

```
app/
├── base/              # shared, environment-agnostic resources
│   ├── kustomization.yaml
│   └── deployment.yaml
├── staging/           # overlay for staging
│   ├── kustomization.yaml
│   └── patch.yaml
└── prod/              # overlay for production
    ├── kustomization.yaml
    └── patch.yaml
```

The `base` directory contains resources that are common to all environments. Overlays
add or override fields without editing the base files.

---

