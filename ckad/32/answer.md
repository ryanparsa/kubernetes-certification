## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/service/#type-clusterip

### Create the namespace (if not present)

```bash
kubectl create namespace networking --dry-run=client -o yaml | kubectl apply -f -
```

### Create the ClusterIP service

```yaml
# lab/internal-app.yaml
apiVersion: v1
kind: Service
metadata:
  name: internal-app
  namespace: networking
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
```

```bash
kubectl apply -f lab/internal-app.yaml
```

### Verify

```bash
kubectl get svc internal-app -n networking
kubectl describe svc internal-app -n networking
```

## Checklist (Score: 0/3)

- [ ] Service `internal-app` exists in namespace `networking` with type `ClusterIP`
- [ ] Service selector matches pods with label `app=backend`
- [ ] Service listens on port `80` and forwards to target port `8080`
