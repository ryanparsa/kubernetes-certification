## Answer

**Reference:** <https://kubernetes.io/docs/concepts/configuration/configmap/#using-configmaps-as-files-from-a-pod>

### Mount the ConfigMap as a volume

Update the Deployment to add the volume and volumeMount:

```bash
kubectl edit deployment web-server
```

Or apply a manifest:

```yaml
# lab/web-server.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-server
spec:
  selector:
    matchLabels:
      app: web-server
  template:
    metadata:
      labels:
        app: web-server
    spec:
      containers:
      - name: web-server
        image: nginx:1.25
        volumeMounts:
        - name: web-server-conf
          mountPath: /etc/nginx/conf.d
      volumes:
      - name: web-server-conf
        configMap:
          name: web-server-conf
```

```bash
kubectl apply -f lab/web-server.yaml
```

### Verify the configuration

```bash
# Wait for the rollout to complete
kubectl rollout status deployment/web-server

# Verify nginx config is valid
POD_NAME=$(kubectl get pod -l app=web-server -o jsonpath='{.items[0].metadata.name}')
kubectl exec $POD_NAME -- nginx -t
```

## Checklist (Score: 0/3)

- [ ] Deployment `web-server` mounts ConfigMap `web-server-conf` as a volume
- [ ] Volume mounted at `/etc/nginx/conf.d`
- [ ] `nginx -t` inside the container passes validation
