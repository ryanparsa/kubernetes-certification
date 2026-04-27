# ConfigMaps and Secrets Reference — 5. TLS Secret in an Ingress

> Part of [ConfigMaps and Secrets Reference](../ConfigMaps and Secrets Reference.md)


```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
  namespace: my-app
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded cert>
  tls.key: <base64-encoded key>
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  namespace: my-app
spec:
  tls:
  - hosts:
    - app.example.com
    secretName: tls-secret
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```

---

