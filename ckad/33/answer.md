## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport

### Create the namespace (if not present)

```bash
kubectl create namespace networking --dry-run=client -o yaml | kubectl apply -f -
```

### Create the NodePort service

```yaml
# lab/public-web.yaml
apiVersion: v1
kind: Service
metadata:
  name: public-web
  namespace: networking
spec:
  type: NodePort
  selector:
    app: web-frontend
  ports:
  - name: http
    protocol: TCP
    port: 80
    targetPort: 8080
    nodePort: 30080
```

```bash
kubectl apply -f lab/public-web.yaml
```

### Verify

```bash
kubectl get svc public-web -n networking
kubectl describe svc public-web -n networking
```

## Checklist (Score: 0/3)

- [ ] Service `public-web` exists in namespace `networking` with type `NodePort`
- [ ] Service selector matches pods with label `app=web-frontend`
- [ ] Service listens on port `80`, forwards to target port `8080`, and exposes NodePort `30080`
