# Hints — Task 11

## Solution

```bash
helm install frontend ./charts/web \
  --namespace platform \
  --set replicaCount=3 \
  --set serviceType=NodePort

helm list -n platform
kubectl -n platform get deployment frontend
kubectl -n platform get svc frontend
```

You can also use a values override file via `-f my-values.yaml`.
