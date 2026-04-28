## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

### Create the namespace

```bash
kubectl create namespace dev
```

### Create the deployment

```bash
kubectl create deployment nginx-deployment -n dev --image=nginx:latest --replicas=3
```

### Verify

```bash
kubectl get deployment nginx-deployment -n dev
kubectl get pods -n dev
```

## Checklist (Score: 0/4)

- [ ] Namespace `dev` exists
- [ ] Deployment `nginx-deployment` exists in namespace `dev`
- [ ] Deployment uses image `nginx:latest`
- [ ] Deployment has 3 replicas running
