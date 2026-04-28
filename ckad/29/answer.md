## Answer

**Reference:** https://helm.sh/docs/intro/using_helm/

### Add the Bitnami Helm repository

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### Create the namespace

```bash
kubectl create namespace web --dry-run=client -o yaml | kubectl apply -f -
```

### Install the Bitnami nginx chart with 2 replicas

```bash
helm install nginx bitnami/nginx --namespace web --set replicaCount=2
```

### Verify

```bash
helm list -n web
kubectl get pods -n web
kubectl get svc -n web
```

## Checklist (Score: 0/2)

- [ ] Bitnami Helm repository is added
- [ ] Bitnami `nginx` chart is deployed in namespace `web` with `2` replicas
