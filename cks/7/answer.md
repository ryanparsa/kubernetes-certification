## Answer

**Reference:** https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#opt-out-of-api-credential-automounting

### Create the namespace and ServiceAccount

```bash
kubectl create namespace service-account-caution
```

### Create the ServiceAccount with automounting disabled

```yaml
# lab/minimal-sa.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: minimal-sa
  namespace: service-account-caution
automountServiceAccountToken: false
```

```bash
kubectl apply -f lab/minimal-sa.yaml
```

### Create the Deployment

```yaml
# lab/secure-app-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
  namespace: service-account-caution
spec:
  replicas: 2
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      serviceAccountName: minimal-sa
      automountServiceAccountToken: false
      containers:
      - name: nginx
        image: nginx
```

```bash
kubectl apply -f lab/secure-app-deployment.yaml
kubectl rollout status deployment secure-app -n service-account-caution
```

### Verify

```bash
kubectl get serviceaccount minimal-sa -n service-account-caution -o jsonpath='{.automountServiceAccountToken}'
# should output: false

kubectl get deployment secure-app -n service-account-caution
kubectl get pods -n service-account-caution -o jsonpath='{.items[0].spec.automountServiceAccountToken}'
# should output: false
```

> [!NOTE]
> Setting `automountServiceAccountToken: false` at both the ServiceAccount and Pod/Deployment spec levels ensures the token is never mounted, even if a future default changes.

## Checklist (Score: 0/5)

- [ ] ServiceAccount `minimal-sa` exists in namespace `service-account-caution`
- [ ] ServiceAccount has `automountServiceAccountToken: false`
- [ ] Deployment `secure-app` exists with 2 replicas in namespace `service-account-caution`
- [ ] Deployment uses ServiceAccount `minimal-sa`
- [ ] Pod template spec has `automountServiceAccountToken: false`
