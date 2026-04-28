## Answer

**Reference:** https://kubernetes.io/docs/concepts/configuration/configmap/

### Create the namespace

```bash
kubectl create namespace pod-configuration
```

### Create the ConfigMap

```bash
kubectl create configmap app-config -n pod-configuration \
  --from-literal=DB_HOST=db.example.com \
  --from-literal=DB_PORT=5432
```

### Create the Secret

```bash
kubectl create secret generic app-secret -n pod-configuration \
  --from-literal=API_KEY=my-api-key \
  --from-literal=API_SECRET=my-api-secret
```

### Create the Pod

```yaml
# lab/56.yaml
apiVersion: v1
kind: Pod
metadata:
  name: config-pod
  namespace: pod-configuration
spec:
  containers:
  - name: nginx
    image: nginx
    env:
    - name: APP_ENV
      value: production
    - name: DEBUG
      value: "false"
    - name: DB_HOST
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: DB_HOST
    - name: DB_PORT
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: DB_PORT
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: API_KEY
    - name: API_SECRET
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: API_SECRET
    volumeMounts:
    - name: config-volume
      mountPath: /etc/app-config
  volumes:
  - name: config-volume
    configMap:
      name: app-config
```

```bash
kubectl apply -f lab/56.yaml
kubectl wait pod/config-pod -n pod-configuration --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl exec config-pod -n pod-configuration -- env | grep -E 'APP_ENV|DEBUG|DB_|API_'
kubectl exec config-pod -n pod-configuration -- ls /etc/app-config
```

## Checklist (Score: 0/5)

- [ ] Namespace `pod-configuration` exists
- [ ] ConfigMap `app-config` has `DB_HOST=db.example.com` and `DB_PORT=5432`
- [ ] Secret `app-secret` has `API_KEY` and `API_SECRET`
- [ ] Pod `config-pod` has correct direct env vars (`APP_ENV=production`, `DEBUG=false`) and env vars from ConfigMap and Secret
- [ ] Pod mounts ConfigMap `app-config` as a volume at `/etc/app-config`
