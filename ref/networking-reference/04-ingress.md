# Kubernetes Networking Reference — 4. Ingress

> Part of [Kubernetes Networking Reference](../Networking Reference.md)


Ingress routes external HTTP/HTTPS traffic to Services based on host and path rules.
Requires an Ingress Controller (nginx, traefik, etc.) to be installed.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  namespace: my-app
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
  tls:
  - hosts:
    - app.example.com
    secretName: tls-secret
```

---

