# Helm Reference

Comprehensive reference for Helm: chart management, release lifecycle, values, templating,
and how Helm interacts with Kubernetes. The CKA exam uses Helm to install operators and
chart-based workloads.

---

## 1. Core Concepts

| Concept | Description |
|---|---|
| **Chart** | Package of pre-configured Kubernetes resources (tarball + templates) |
| **Release** | A running instance of a chart in a cluster; identified by name + namespace |
| **Repository** | HTTP server hosting an `index.yaml` that lists available charts |
| **Values** | Key-value configuration that gets injected into chart templates |
| **Revision** | Each `install` or `upgrade` creates a new numbered revision for a release |

Helm stores release state as **Secrets** (default) in the release namespace. Each revision
is one Secret with `type=helm.sh/release.v1`.

---

## 2. Repository Management

```bash
# Add a repository
helm repo add <name> <url>
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add minio   https://operator.min.io/

# List configured repositories
helm repo list

# Update local index cache (like apt-get update)
helm repo update

# Remove a repository
helm repo remove <name>
```

---

## 3. Searching Charts

```bash
# Search all configured repos for a chart
helm search repo <keyword>
helm search repo minio

# Search with version info
helm search repo nginx --versions

# Search Artifact Hub (public registry - requires internet)
helm search hub <keyword>

# Show all available chart versions
helm search repo bitnami/nginx --versions
```

---

## 4. Inspecting a Chart Before Installing

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

## 5. Installing a Chart

```bash
# Basic install - release name + chart
helm install <release-name> <chart>
helm install my-nginx bitnami/nginx

# Install into a specific namespace (creates namespace if it doesn't exist with --create-namespace)
helm install my-nginx bitnami/nginx \
  --namespace ingress \
  --create-namespace

# Install a specific chart version
helm install my-nginx bitnami/nginx --version 15.0.0

# Override values inline (--set)
helm install my-release bitnami/nginx \
  --set replicaCount=3 \
  --set service.type=ClusterIP

# Override values with a file (--values / -f)
helm install my-release bitnami/nginx \
  --values custom-values.yaml

# Combine --set and -f (--set overrides -f values)
helm install my-release bitnami/nginx \
  -f base-values.yaml \
  --set image.tag=1.25

# Dry-run (render templates without installing)
helm install my-release bitnami/nginx --dry-run

# Install a local chart directory
helm install my-release ./my-chart/

# Install a local chart tarball
helm install my-release ./my-chart-1.0.0.tgz
```

### --set value syntax

```bash
--set key=value                          # simple value
--set a=1,b=2                            # multiple values
--set outer.inner=value                  # nested key
--set list[0]=value                      # list item
--set list[0]=val1,list[1]=val2          # multiple list items
--set "key=value with spaces"            # value with spaces (quote)
--set-string numericKey=123              # force string type
--set-json 'key={"a":1}'                 # JSON value (Helm 3.10+)
```

---

## 6. Listing and Inspecting Releases

```bash
# List all releases in current namespace
helm list
helm ls

# List releases in a specific namespace
helm list -n kube-system
helm ls -n minio

# List releases in all namespaces
helm list -A
helm ls -A

# Show a release's status and metadata
helm status <release-name> -n <namespace>
helm status my-nginx -n ingress

# Show the computed values used by a release
helm get values my-nginx -n ingress

# Show the values including defaults
helm get values my-nginx -n ingress --all

# Show the rendered manifests for a release
helm get manifest my-nginx -n ingress

# Show the chart notes
helm get notes my-nginx -n ingress
```

---

## 7. Upgrading a Release

```bash
# Upgrade to a new chart version
helm upgrade <release-name> <chart>
helm upgrade my-nginx bitnami/nginx

# Upgrade and change values
helm upgrade my-nginx bitnami/nginx \
  --set replicaCount=5

# Upgrade with a values file
helm upgrade my-nginx bitnami/nginx \
  -f custom-values.yaml

# Upgrade or install if not yet installed (--install / -i)
helm upgrade --install my-nginx bitnami/nginx \
  -n ingress --create-namespace

# Upgrade to a specific version
helm upgrade my-nginx bitnami/nginx --version 15.0.0

# Preview changes without applying (--dry-run)
helm upgrade my-nginx bitnami/nginx --dry-run
```

---

## 8. Release History and Rollback

```bash
# View revision history of a release
helm history <release-name> -n <namespace>
helm history my-nginx -n ingress
# REVISION  UPDATED                  STATUS     CHART          APP VERSION  DESCRIPTION
# 1         Mon Jan 01 00:00:00 UTC  superseded nginx-15.0.0   1.25.0       Install complete
# 2         Tue Jan 02 00:00:00 UTC  deployed   nginx-15.1.0   1.25.1       Upgrade complete

# Roll back to the previous revision
helm rollback <release-name>
helm rollback my-nginx

# Roll back to a specific revision
helm rollback my-nginx 1 -n ingress
```

---

## 9. Uninstalling a Release

```bash
# Uninstall a release (removes all resources and the release secret)
helm uninstall <release-name>
helm uninstall my-nginx -n ingress

# Keep release history (can rollback/inspect after uninstall)
helm uninstall my-nginx -n ingress --keep-history

# Dry-run uninstall
helm uninstall my-nginx --dry-run
```

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

## 11. Downloading and Packaging Charts

```bash
# Download a chart tarball to current directory
helm pull bitnami/nginx
# -> nginx-15.1.0.tgz

# Download and extract
helm pull bitnami/nginx --untar

# Download a specific version
helm pull bitnami/nginx --version 15.0.0

# Create a new chart scaffold
helm create my-chart
# -> my-chart/
#     Chart.yaml
#     values.yaml
#     templates/

# Package a local chart directory into a tarball
helm package ./my-chart/
```

---

## 12. How Helm Differs from Kustomize

| Feature | Helm | Kustomize |
|---|---|---|
| Packaging | Self-contained chart tarballs with versioning | Plain YAML patches on top of existing manifests |
| State tracking | Stores release state as Secrets in the cluster | Stateless - no cluster state |
| Templating | Go templates with full logic | Strategic merge patches and JSON patches |
| Rollback | Built-in `helm rollback` per revision | No native rollback (use `git revert`) |
| Values | `values.yaml` + `--set` overrides | `kustomization.yaml` patches |
| Upgrade tracking | Tracks old -> new resources and deletes removed ones | `kubectl apply` - does not delete removed resources |

---

## 13. Working with OCI Registries

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

## 14. Quick Reference

```bash
# Full install workflow
helm repo add minio https://operator.min.io/
helm repo update
helm search repo minio
helm show values minio/operator
helm install minio-operator minio/operator -n minio --create-namespace
helm ls -n minio
helm status minio-operator -n minio
helm get values minio-operator -n minio
```

| Task | Command |
|---|---|
| Add repo | `helm repo add <name> <url>` |
| Update repos | `helm repo update` |
| Search charts | `helm search repo <keyword>` |
| Show default values | `helm show values <chart>` |
| Install | `helm install <release> <chart> -n <ns> --create-namespace` |
| Install+upgrade | `helm upgrade --install <release> <chart> -n <ns>` |
| List releases | `helm ls -A` |
| Release status | `helm status <release> -n <ns>` |
| View values in use | `helm get values <release> -n <ns>` |
| View rendered YAML | `helm get manifest <release> -n <ns>` |
| Upgrade | `helm upgrade <release> <chart> --set key=val` |
| Rollback | `helm rollback <release> [revision]` |
| History | `helm history <release> -n <ns>` |
| Uninstall | `helm uninstall <release> -n <ns>` |
| Dry-run | `helm install <release> <chart> --dry-run` |
| Render templates | `helm template <release> <chart>` |
