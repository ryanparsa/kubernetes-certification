# ConfigMaps and Secrets Reference — 6. Useful Commands

> Part of [ConfigMaps and Secrets Reference](../ConfigMaps and Secrets Reference.md)


```bash
# List ConfigMaps
kubectl get configmap -n my-app

# Describe a ConfigMap (see keys, not values)
kubectl describe configmap app-config -n my-app

# View ConfigMap data
kubectl get configmap app-config -n my-app -o yaml

# Edit a ConfigMap in-place
kubectl edit configmap app-config -n my-app

# List Secrets (values are hidden)
kubectl get secret -n my-app

# Describe a Secret (shows types and data keys, NOT values)
kubectl describe secret db-credentials -n my-app

# Decode a Secret value
kubectl get secret db-credentials -n my-app \
  -o jsonpath='{.data.DB_PASSWORD}' | base64 --decode

# Delete a ConfigMap or Secret
kubectl delete configmap app-config -n my-app
kubectl delete secret db-credentials -n my-app
```

---

