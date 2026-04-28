## Answer

**Reference:** <https://kubernetes.io/docs/concepts/configuration/configmap/#using-configmaps-as-files-from-a-pod>

### Get the existing Deployment

```bash
kubectl get deployment web-server -o yaml > lab/web-server.yaml
kubectl get configmap web-server-conf -o yaml
```

### Mount the ConfigMap as a volume

Edit the Deployment to add the volume and volumeMount:

```yaml
# lab/web-server.yaml (relevant sections)
spec:
  template:
    spec:
      containers:
      - name: web-server
        # existing config...
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
kubectl rollout status deployment/web-server

# Verify nginx config is valid
kubectl exec -it <pod-name> -- nginx -t
```

## Checklist (Score: 0/3)

- [ ] Deployment `web-server` mounts ConfigMap `web-server-conf` as a volume
- [ ] Volume mounted at `/etc/nginx/conf.d`
- [ ] `nginx -t` inside the container passes validation
