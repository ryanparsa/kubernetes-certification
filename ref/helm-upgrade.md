# Upgrading a Release

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

