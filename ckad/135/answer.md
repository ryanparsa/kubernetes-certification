## Answer

**Reference:** <https://kubernetes.io/docs/concepts/cluster-administration/logging/>

### Get the existing Deployment

```bash
kubectl get deployment cleaner -n pluto -o yaml > lab/cleaner.yaml
```

### Add sidecar logger container

Edit the Deployment to add the `logger-col` sidecar and a shared volume:

```yaml
# lab/cleaner.yaml (relevant sections)
spec:
  template:
    spec:
      containers:
      - name: cleaner-con
        # existing container...
        volumeMounts:
        - name: logs
          mountPath: /var/log/cleaner
      - name: logger-col
        image: busybox:1.31.0
        command: ["sh", "-c", "tail -f /var/log/cleaner/cleaner.log"]
        volumeMounts:
        - name: logs
          mountPath: /var/log/cleaner
      volumes:
      - name: logs
        emptyDir: {}
```

```bash
kubectl apply -f lab/cleaner.yaml
kubectl rollout status deployment/cleaner -n pluto

# View sidecar logs
kubectl logs -n pluto <pod-name> -c logger-col
```

## Checklist (Score: 0/4)

- [ ] Deployment `cleaner` in Namespace `pluto` updated with sidecar `logger-col`
- [ ] Sidecar uses image `busybox:1.31.0`
- [ ] Sidecar and main container share a volume mounted at `/var/log/cleaner`
- [ ] `kubectl logs -c logger-col` shows log content from `/var/log/cleaner/cleaner.log`
