## Answer

**Reference:** https://kubernetes.io/docs/concepts/cluster-administration/logging/

### Create the namespace and pod

```bash
kubectl create namespace log-namespace
kubectl run log-pod --image=nginx -n log-namespace
kubectl wait pod/log-pod -n log-namespace --for=condition=Ready --timeout=60s
```

### Retrieve logs for the last hour

```bash
kubectl logs --since=1h log-pod -n log-namespace
```

### Additional useful log commands

```bash
# Stream logs in real time
kubectl logs -f log-pod -n log-namespace

# Show last 20 lines
kubectl logs --tail=20 log-pod -n log-namespace

# Logs from previous container instance (if crashed)
kubectl logs -p log-pod -n log-namespace
```

## Checklist (Score: 0/2)

- [ ] Pod `log-pod` exists in `log-namespace` and is `Running`
- [ ] Logs retrieved using `--since=1h` flag
