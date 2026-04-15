# Hints — Task 17

## Solution

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
  namespace: observability
spec:
  selector:
    matchLabels: { app: node-exporter }
  template:
    metadata:
      labels: { app: node-exporter }
    spec:
      nodeSelector:
        monitoring: "true"
      containers:
      - name: exporter
        image: nginx:1.27-alpine
```

`nodeSelector` is the simplest way to constrain a DaemonSet. `nodeAffinity` works too.
