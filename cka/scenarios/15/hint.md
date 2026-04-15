# Hints — Task 15

## Solution

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
  namespace: app
spec:
  containers:
  - name: web
    image: nginx:1.27-alpine
    env:
    - name: LOG_LEVEL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: LOG_LEVEL
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: DB_PASSWORD
    volumeMounts:
    - name: cfg
      mountPath: /etc/config
      readOnly: true
    - name: sec
      mountPath: /etc/secret
  volumes:
  - name: cfg
    configMap:
      name: app-config
  - name: sec
    secret:
      secretName: app-secret
      defaultMode: 0400
```
