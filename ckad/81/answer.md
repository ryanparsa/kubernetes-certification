## Answer

**Reference:** https://kubernetes.io/docs/concepts/configuration/configmap/

### Create the namespace

```bash
kubectl create namespace config-test
```

### Create the ConfigMap

```bash
kubectl create configmap app-config \
  --from-literal=DATABASE_HOST=postgres.default.svc.cluster.local \
  --from-literal=DATABASE_PORT=5432 \
  --from-literal=LOG_LEVEL=debug \
  -n config-test
```

### Create the Pod using envFrom

```yaml
# lab/config-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: config-pod
  namespace: config-test
spec:
  containers:
  - name: app
    image: alpine
    command: ["sleep", "3600"]
    envFrom:
    - configMapRef:
        name: app-config
```

```bash
kubectl apply -f lab/config-pod.yaml
kubectl wait pod/config-pod -n config-test --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl exec config-pod -n config-test -- env | grep DATABASE
# Expected:
# DATABASE_HOST=postgres.default.svc.cluster.local
# DATABASE_PORT=5432
```

## Checklist (Score: 0/3)

- [ ] ConfigMap `app-config` exists in namespace `config-test` with keys `DATABASE_HOST`, `DATABASE_PORT`, and `LOG_LEVEL`
- [ ] Pod `config-pod` in namespace `config-test` is Running
- [ ] Environment variables from `app-config` are present inside the container
