## Answer

**Reference:** <https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/>

### Get the existing Deployment

```bash
kubectl get deployment pluto-deployment -n pluto -o yaml > lab/pluto-deployment.yaml
```

### Add sidecar container

Edit the Deployment spec to add the sidecar container and shared volume:

```yaml
# lab/pluto-deployment.yaml (relevant sections)
spec:
  template:
    spec:
      containers:
      - name: pluto-app
        # existing container config...
        volumeMounts:
        - name: log-data
          mountPath: /tmp/log
      - name: sidecar
        image: busybox:1.31.0
        command: ["sh", "-c", "while true; do date >> /var/log/date.log; sleep 1; done"]
        volumeMounts:
        - name: log-data
          mountPath: /var/log
      volumes:
      - name: log-data
        emptyDir: {}
```

```bash
kubectl apply -f lab/pluto-deployment.yaml
kubectl get pods -n pluto
kubectl logs <pod-name> -n pluto -c sidecar
```

## Checklist (Score: 0/4)

- [ ] Deployment `pluto-deployment` updated with sidecar container named `sidecar`
- [ ] Sidecar uses image `busybox:1.31.0`
- [ ] Sidecar runs `while true; do date >> /var/log/date.log; sleep 1; done`
- [ ] Both containers share volume `log-data` at correct mount paths
