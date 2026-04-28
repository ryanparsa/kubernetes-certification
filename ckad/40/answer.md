## Answer

**Reference:** https://kubernetes.io/docs/concepts/configuration/configmap/

### Create the *Namespace*

```bash
kubectl create namespace configuration
```

### Create the *ConfigMap*

```bash
kubectl create configmap app-config -n configuration \
  --from-literal=DB_HOST=mysql \
  --from-literal=DB_PORT=3306 \
  --from-literal=DB_NAME=myapp
```

### Create the *Secret*

```bash
kubectl create secret generic app-secret -n configuration \
  --from-literal=DB_USER=admin \
  --from-literal=DB_PASSWORD=s3cr3t
```

### Create the *Pod* using *ConfigMap* and *Secret*

```yaml
# lab/40.yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
  namespace: configuration
spec:
  containers:
  - name: nginx
    image: nginx
    envFrom:
    - configMapRef:
        name: app-config
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/app-secret
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: app-secret
```

```bash
kubectl apply -f lab/40.yaml
kubectl wait pod/app-pod -n configuration --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl exec app-pod -n configuration -- env | grep DB_
kubectl exec app-pod -n configuration -- ls /etc/app-secret
```

## Checklist (Score: 0/5)

- [ ] *Namespace* `configuration` exists
- [ ] *ConfigMap* `app-config` has correct data (`DB_HOST`, `DB_PORT`, `DB_NAME`)
- [ ] *Secret* `app-secret` has correct data (`DB_USER`, `DB_PASSWORD`)
- [ ] *Pod* `app-pod` uses *ConfigMap* as environment variables
- [ ] *Pod* `app-pod` mounts *Secret* as *Volume* at `/etc/app-secret`
