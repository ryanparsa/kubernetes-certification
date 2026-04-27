# Kubernetes Workloads Reference

[← Back to index](../README.md)

---

## 9. Sidecar Containers

A sidecar runs **alongside** the main container throughout the pod lifetime. In
Kubernetes 1.29+ there is a native sidecar container type (`initContainers` with
`restartPolicy: Always`) that starts before app containers and stops after them.

### Classic sidecar (just an extra container)

```yaml
spec:
  containers:
  - name: app
    image: my-app:v1
  - name: log-shipper
    image: fluentbit:latest
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
```

### Native sidecar (Kubernetes 1.29+)

```yaml
spec:
  initContainers:
  - name: log-shipper
    image: fluentbit:latest
    restartPolicy: Always       # marks this as a sidecar — starts before app containers
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
  containers:
  - name: app
    image: my-app:v1
```

> Native sidecars are included in HPA scaling decisions and are properly ordered during
> pod start/stop, unlike classic sidecars.

---
