## Answer

**Reference:** https://kubernetes.io/docs/concepts/security/pod-security-admission/

### Create the namespace with PSA enforcement

```bash
kubectl create namespace security
kubectl label namespace security \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/enforce-version=latest
```

### Create the secure pod

```yaml
# lab/53-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
  namespace: security
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: nginx
    image: nginx
    securityContext:
      allowPrivilegeEscalation: false
      runAsNonRoot: true
      runAsUser: 1000
      capabilities:
        drop:
          - ALL
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
  volumes:
  - name: html
    emptyDir: {}
```

```bash
kubectl apply -f lab/53-pod.yaml
kubectl wait pod secure-pod -n security --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl get pod secure-pod -n security
kubectl get namespace security --show-labels
```

## Checklist (Score: 0/8)

- [ ] Namespace `security` exists with PSA label `enforce=restricted`
- [ ] Pod `secure-pod` exists in `security` namespace
- [ ] Pod uses `nginx` image
- [ ] Pod-level security context sets `runAsUser: 1000` and `runAsNonRoot: true`
- [ ] Pod-level security context uses `seccompProfile: RuntimeDefault`
- [ ] Container sets `allowPrivilegeEscalation: false`
- [ ] Container drops ALL capabilities
- [ ] `emptyDir` volume `html` is mounted at `/usr/share/nginx/html`
