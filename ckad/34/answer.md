## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/ingress/

### Create the namespace (if not present)

```bash
kubectl create namespace networking --dry-run=client -o yaml | kubectl apply -f -
```

### Create the Ingress resource

```yaml
# lab/api-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  namespace: networking
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```

```bash
kubectl apply -f lab/api-ingress.yaml
```

### Verify

```bash
kubectl get ingress api-ingress -n networking
kubectl describe ingress api-ingress -n networking
```

## Checklist (Score: 0/3)

- [ ] *Ingress* `api-ingress` exists in *Namespace* `networking`
- [ ] *Ingress* routes traffic for host `api.example.com`
- [ ] *Ingress* backend points to *Service* `api-service` on port `80`
