## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/ingress/#tls

### Create the TLS Ingress

```yaml
# lab/secure-app-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: secure-app
  namespace: secure-ingress
spec:
  tls:
  - hosts:
    - secure-app.example.com
    secretName: secure-app-tls
  rules:
  - host: secure-app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

```bash
kubectl apply -f lab/secure-app-ingress.yaml
```

### Verify

```bash
kubectl get ingress secure-app -n secure-ingress
kubectl describe ingress secure-app -n secure-ingress
```

The Ingress should show:
- Host: `secure-app.example.com`
- TLS Secret: `secure-app-tls`
- Backend: `web-service:80`

## Checklist (Score: 0/5)

- [ ] Ingress `secure-app` exists in namespace `secure-ingress`
- [ ] Ingress responds to hostname `secure-app.example.com`
- [ ] Ingress has TLS block referencing secret `secure-app-tls`
- [ ] TLS block includes host `secure-app.example.com`
- [ ] Backend routes to service `web-service` on port 80
