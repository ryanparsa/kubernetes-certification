# How Helm Differs from Kustomize

| Feature | Helm | Kustomize |
|---|---|---|
| Packaging | Self-contained chart tarballs with versioning | Plain YAML patches on top of existing manifests |
| State tracking | Stores release state as Secrets in the cluster | Stateless — no cluster state |
| Templating | Go templates with full logic | Strategic merge patches and JSON patches |
| Rollback | Built-in `helm rollback` per revision | No native rollback (use `git revert`) |
| Values | `values.yaml` + `--set` overrides | `kustomization.yaml` patches |
| Upgrade tracking | Tracks old → new resources and deletes removed ones | `kubectl apply` — does not delete removed resources |

---

