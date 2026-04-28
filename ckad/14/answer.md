## Answer

**Reference:** https://helm.sh/docs/helm/helm_install/

### Add the Bitnami repo

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm repo list
```

### Search and show chart values

```bash
helm search repo bitnami/nginx
helm show values bitnami/nginx | head -60
```

### Install my-nginx with replicaCount=2

```bash
kubectl create namespace helm-demo
helm install my-nginx bitnami/nginx \
  --namespace helm-demo \
  --set replicaCount=2
```

Wait for the release to be ready:

```bash
helm status my-nginx -n helm-demo
kubectl get pods -n helm-demo
kubectl get deployment -n helm-demo
```

### Upgrade to replicaCount=3

```bash
helm upgrade my-nginx bitnami/nginx \
  --namespace helm-demo \
  --set replicaCount=3

kubectl rollout status deployment -n helm-demo
kubectl get deployment -n helm-demo
```

The deployment should show `3/3` ready replicas.

### Uninstall the release

```bash
helm uninstall my-nginx --namespace helm-demo
helm list -n helm-demo
kubectl get pods -n helm-demo
```

After uninstall, `helm list` should return no entries for `helm-demo`.

## Checklist (Score: 0/5)

- [ ] Bitnami repo added and updated successfully
- [ ] `helm show values bitnami/nginx` displays chart values
- [ ] Release `my-nginx` installed in `helm-demo` with 2 replicas
- [ ] Release `my-nginx` upgraded to 3 replicas
- [ ] Release `my-nginx` uninstalled and no longer listed
