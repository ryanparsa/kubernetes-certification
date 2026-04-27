# Quick Reference

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
