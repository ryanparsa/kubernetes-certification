# Kustomize Reference

Reference for Kustomize: the built-in Kubernetes configuration management tool that
lets you customise YAML files without forking them. Included in `kubectl` as
`kubectl kustomize` / `kubectl apply -k`.

---

## 1. Core Concept

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

## 2. `kustomization.yaml` Structure

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

## 3. Patches

Two patch formats are supported:

### Strategic Merge Patch

Looks like a partial Kubernetes resource. Kubernetes merges it using strategic merge rules
(lists are merged by name/key, not replaced wholesale).

```yaml
# replica-patch.yaml (strategic merge patch)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway          # must match the target resource
spec:
  replicas: 4                # overrides the base value
  template:
    spec:
      containers:
      - name: httpd
        resources:
          requests:
            cpu: 200m
```

Reference in `kustomization.yaml`:

```yaml
patches:
  - path: replica-patch.yaml
```

### JSON6902 Patch (RFC 6902)

Precise, operation-based. Useful when strategic merge doesn't work (e.g. removing array elements).

Operations: `add`, `remove`, `replace`, `move`, `copy`, `test`

```yaml
# json6902-patch.yaml
- op: replace
  path: /spec/replicas
  value: 6
- op: add
  path: /spec/template/spec/containers/0/env/-
  value:
    name: ENV
    value: production
- op: remove
  path: /spec/template/spec/containers/0/resources
```

Reference in `kustomization.yaml`:

```yaml
patches:
  - target:
      kind: Deployment
      name: api-gateway
    path: json6902-patch.yaml
```

Or inline:

```yaml
patches:
  - target:
      kind: Deployment
      name: api-gateway
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 6
```

### Strategic Merge vs JSON6902

| | Strategic Merge | JSON6902 |
|---|---|---|
| Format | Partial resource YAML | Operations list |
| List handling | Smart (merge by key) | Replace entire list by default |
| Removing fields | Tricky — use `$patch: delete` | Clean: `op: remove` |
| Cross-kind patches | No | Yes (target specifies kind/name) |
| Readability | High | Lower |
| Use case | Field overrides, replica counts, image tags | Precise array manipulation, deletions |

---

## 4. Generators

Generators create ConfigMaps or Secrets and automatically append a content hash to
the name (e.g. `app-config-k8d9f2m`). This triggers a rolling update whenever the
data changes.

### ConfigMap generator

```yaml
configMapGenerator:
  - name: app-config
    files:
    - config.properties           # key = filename, value = file contents
    - app.conf=myconfig.conf       # custom key name
    literals:
    - LOG_LEVEL=info
    - MAX_RETRIES=3
    options:
      disableNameSuffixHash: true  # keep original name (no hash)
      labels:
        app: my-app
```

### Secret generator

```yaml
secretGenerator:
  - name: db-credentials
    literals:
    - DB_USER=admin
    - DB_PASSWORD=s3cr3t
    type: Opaque
    options:
      disableNameSuffixHash: true
  - name: tls-secret
    files:
    - tls.crt
    - tls.key
    type: kubernetes.io/tls
```

> When you change a ConfigMap or Secret value, the hash suffix changes, which causes
> the Deployment to see a new volume/env source and roll out automatically.

---

## 5. Image Overrides

Change image names and tags without editing deployment YAML:

```yaml
images:
  - name: my-app              # matches .spec.containers[*].image by name
    newTag: v2.1.0
  - name: nginx
    newName: registry.example.com/nginx
    newTag: 1.25-alpine
```

---

## 6. `kubectl kustomize` vs `kubectl apply -k`

| Command | Effect |
|---|---|
| `kubectl kustomize <dir>` | Build and print YAML to stdout — does NOT apply to cluster |
| `kubectl apply -k <dir>` | Build and apply to cluster in one step |
| `kubectl kustomize <dir> \| kubectl apply -f -` | Equivalent to `apply -k` but allows `--dry-run` or `diff` in between |
| `kubectl kustomize <dir> \| kubectl diff -f -` | Preview what would change |
| `kubectl delete -k <dir>` | Delete all resources in the built YAML |

```bash
# Preview what would be applied
kubectl kustomize staging | kubectl diff -f -

# Apply staging overlay
kubectl kustomize staging | kubectl apply -f -
# or
kubectl apply -k staging

# Apply prod overlay
kubectl apply -k prod

# Check the built output before applying
kubectl kustomize prod | less

# Apply and watch rollout
kubectl apply -k prod && kubectl rollout status deployment/api-gateway -n api-gateway-prod
```

---

## 7. Directory Layout Patterns

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

## 8. State and Lifecycle

**Kustomize does not track state.** It does not know which resources it previously created.

- Adding a resource to kustomize YAML and applying → resource is created
- Removing a resource from kustomize YAML and applying → resource is **NOT deleted**
  (you must delete it manually with `kubectl delete`)

This is different from Helm, which tracks state in a release and deletes removed resources.

```bash
# Kustomize won't delete this — must be done manually
kubectl delete configmap horizontal-scaling-config -n api-gateway-staging
kubectl delete configmap horizontal-scaling-config -n api-gateway-prod
```

---

## 9. Debugging Tips

```bash
# Build and validate without applying
kubectl kustomize staging

# Common error: patch target not found in base
# → The resource referenced by the patch doesn't exist in resources
# Fix: make sure the resource is in base/ and patch metadata.name matches exactly

# Check what a full build produces for an overlay
kubectl kustomize prod | grep -A 5 "kind: HorizontalPodAutoscaler"

# Validate with dry-run
kubectl kustomize prod | kubectl apply --dry-run=client -f -

# Diff against live cluster
kubectl kustomize prod | kubectl diff -f -
```
