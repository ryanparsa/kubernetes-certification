# Kustomize Reference — 2. `kustomization.yaml` Structure

> Part of [Kustomize Reference](../Kustomize Reference.md)


Every directory managed by Kustomize must contain a `kustomization.yaml` file.

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

# --- Resources to include ---
resources:
  - ../base               # reference to another directory (the base)
  - extra-service.yaml    # additional resource file

# --- Namespace for all resources ---
namespace: my-app-staging

# --- Common labels added to all resources ---
commonLabels:
  env: staging

# --- Common annotations added to all resources ---
commonAnnotations:
  team: backend

# --- Name prefix/suffix for all resources ---
namePrefix: staging-
nameSuffix: -v2

# --- Patches ---
patches:
  - path: replica-patch.yaml                   # strategic merge patch (default)
  - path: deployment-image-patch.yaml
  - target:                                    # inline JSON6902 patch
      kind: Deployment
      name: api-gateway
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 4

# --- ConfigMap generator ---
configMapGenerator:
  - name: app-config
    files:
    - config.properties
    literals:
    - LOG_LEVEL=info

# --- Secret generator ---
secretGenerator:
  - name: db-secret
    literals:
    - DB_PASSWORD=s3cr3t
    type: Opaque

# --- Image overrides ---
images:
  - name: my-app
    newTag: v2.0.0
    # newName: registry.example.com/my-app   # optional: also change registry/name

# --- Transformers (inline) ---
transformers:
  - |-
    apiVersion: builtin
    kind: NamespaceTransformer
    metadata:
      name: notImportantHere
      namespace: api-gateway-staging
```

---

