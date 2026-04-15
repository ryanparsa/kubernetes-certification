# Hints — Task 7

## Hint 1
Without **both** the toleration and the affinity, you'll either get pods stuck on the
control-plane node (no taint, but no `disk=ssd` label) or stuck `Pending`.

## Solution

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: priority-app
spec:
  replicas: 3
  selector: { matchLabels: { app: priority-app } }
  template:
    metadata: { labels: { app: priority-app } }
    spec:
      tolerations:
      - key: tier
        operator: Equal
        value: critical
        effect: NoSchedule
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: disk
                operator: In
                values: [ssd]
      containers:
      - name: app
        image: nginx:1.27-alpine
        resources:
          requests: { cpu: 100m }
          limits:   { cpu: 200m }
```
