## Answer

**Reference:** https://kubernetes.io/docs/concepts/configuration/configmap/

### Create the ConfigMap

```bash
kubectl create configmap app-config --from-literal=ENV=production --from-literal=LOG_LEVEL=info
kubectl describe configmap app-config
```

### Pod cm-env — load all keys as environment variables

```yaml
# lab/cm-env.yaml
apiVersion: v1
kind: Pod
metadata:
  name: cm-env
spec:
  containers:
  - name: nginx
    image: nginx
    envFrom:
    - configMapRef:
        name: app-config
```

```bash
kubectl apply -f lab/cm-env.yaml
kubectl exec cm-env -- printenv ENV
kubectl exec cm-env -- printenv LOG_LEVEL
```

Expected: `production` and `info`

### Pod cm-vol — mount ConfigMap as a volume

```yaml
# lab/cm-vol.yaml
apiVersion: v1
kind: Pod
metadata:
  name: cm-vol
spec:
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: config-vol
      mountPath: /etc/config
  volumes:
  - name: config-vol
    configMap:
      name: app-config
```

```bash
kubectl apply -f lab/cm-vol.yaml
kubectl exec cm-vol -- ls /etc/config
kubectl exec cm-vol -- cat /etc/config/ENV
kubectl exec cm-vol -- cat /etc/config/LOG_LEVEL
```

Expected files: `ENV` (content `production`) and `LOG_LEVEL` (content `info`)

## Checklist (Score: 0/3)

- [ ] ConfigMap `app-config` exists with keys `ENV=production` and `LOG_LEVEL=info`
- [ ] Pod `cm-env` has `ENV` and `LOG_LEVEL` available as environment variables via `envFrom`
- [ ] Pod `cm-vol` has files `/etc/config/ENV` and `/etc/config/LOG_LEVEL` from volume mount
