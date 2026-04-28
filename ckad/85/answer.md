## Answer

**Reference:** https://kubernetes.io/docs/tasks/configure-pod-container/security-context/

### Create the namespace and ConfigMap

```bash
kubectl create namespace secure
kubectl create configmap app-config --from-literal=key=value -n secure
```

### Create the Pod with SecurityContext

```yaml
# lab/secure-app.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  namespace: secure
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
  - name: app
    image: alpine
    command: ["sleep", "3600"]
    securityContext:
      capabilities:
        drop:
        - ALL
      readOnlyRootFilesystem: true
      allowPrivilegeEscalation: false
    volumeMounts:
    - name: config-vol
      mountPath: /config
  volumes:
  - name: config-vol
    configMap:
      name: app-config
```

```bash
kubectl apply -f lab/secure-app.yaml
kubectl wait pod/secure-app -n secure --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl get pod secure-app -n secure -o yaml | grep -A 12 "securityContext"
# Pod-level: runAsUser 1000, runAsGroup 3000, fsGroup 2000
# Container-level: readOnlyRootFilesystem true, allowPrivilegeEscalation false, drop ALL
```

## Checklist (Score: 0/4)

- [ ] Pod `secure-app` in namespace `secure` is Running
- [ ] Pod-level SecurityContext sets `runAsUser: 1000`, `runAsGroup: 3000`, `fsGroup: 2000`
- [ ] Container-level SecurityContext drops all capabilities, sets `readOnlyRootFilesystem: true` and `allowPrivilegeEscalation: false`
- [ ] ConfigMap `app-config` is mounted as a volume at `/config`
