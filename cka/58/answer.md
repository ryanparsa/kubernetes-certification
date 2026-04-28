## Answer

**Reference:** https://helm.sh/docs/intro/using_helm/

### Add the Bitnami Helm repository

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### Create the namespace and install the chart

```bash
kubectl create namespace helm-test

helm install web-release bitnami/nginx \
  --namespace helm-test \
  --set service.type=NodePort \
  --set replicaCount=2
```

### Verify

```bash
helm status web-release -n helm-test
kubectl get deployment -n helm-test
kubectl get pods -n helm-test
kubectl get svc -n helm-test
```

## Checklist (Score: 0/5)

- [ ] Bitnami repo is added and updated
- [ ] Helm release `web-release` is installed in `helm-test` namespace
- [ ] Release is from the `bitnami/nginx` chart
- [ ] Service type is `NodePort`
- [ ] Replica count is `2` and pods are `Running`
