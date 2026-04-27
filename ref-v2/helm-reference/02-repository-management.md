# Helm Reference

[← Back to index](../README.md)

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
