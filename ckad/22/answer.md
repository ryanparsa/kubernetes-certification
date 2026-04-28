## Answer

**Reference:** https://kubernetes.io/docs/concepts/services-networking/service/

### Investigate the service

```bash
# Check the service configuration
kubectl get svc web-service -n troubleshooting -o yaml

# Check pod labels in the namespace
kubectl get pods -n troubleshooting --show-labels

# Check if the service has any endpoints
kubectl get endpoints web-service -n troubleshooting
```

### Fix the service selector

If the service selector does not match pod labels, patch the selector:

```yaml
# lab/web-service-fix.yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
  namespace: troubleshooting
spec:
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 80
```

```bash
kubectl apply -f lab/web-service-fix.yaml
```

### Verify

```bash
kubectl get endpoints web-service -n troubleshooting
```

Endpoints should be populated with pod IPs.

## Checklist (Score: 0/2)

- [ ] Service `web-service` selector matches the labels on the target pods
- [ ] Service port configuration matches the container ports on the target pods
