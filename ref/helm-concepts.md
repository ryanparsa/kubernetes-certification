# Core Concepts

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

