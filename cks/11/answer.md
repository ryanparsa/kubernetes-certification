## Answer

**Reference:** https://kubernetes.io/docs/concepts/security/pod-security-admission/

### Label the namespace to enforce baseline PSS

```bash
kubectl label namespace pod-security pod-security.kubernetes.io/enforce=baseline
```

Verify:

```bash
kubectl get namespace pod-security --show-labels
```

### Create a compliant pod

A `baseline` Pod Security Standard prohibits `privileged` containers, `hostPID/hostIPC/hostNetwork`, and specific volume types. A plain nginx pod is compliant:

```yaml
# lab/compliant-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: compliant-pod
  namespace: pod-security
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
  containers:
  - name: nginx
    image: nginx
    securityContext:
      allowPrivilegeEscalation: false
```

```bash
kubectl apply -f lab/compliant-pod.yaml
kubectl wait pod compliant-pod -n pod-security --for=condition=Ready --timeout=60s
```

### Attempt to create a non-compliant pod and document the error

```bash
kubectl apply -f - <<'EOF' 2>&1 | tee /tmp/violation.txt
apiVersion: v1
kind: Pod
metadata:
  name: non-compliant-pod
  namespace: pod-security
spec:
  containers:
  - name: nginx
    image: nginx
    securityContext:
      privileged: true
EOF
```

The command should fail with an error like:
```
Error from server (Forbidden): pods "non-compliant-pod" is forbidden: violates PodSecurity "baseline:latest"
```

### Verify

```bash
kubectl get pod compliant-pod -n pod-security
kubectl get pod non-compliant-pod -n pod-security  # should not exist
cat /tmp/violation.txt
```

## Checklist (Score: 0/5)

- [ ] Namespace `pod-security` has label `pod-security.kubernetes.io/enforce=baseline`
- [ ] Pod `compliant-pod` exists and is Running in namespace `pod-security`
- [ ] Pod `non-compliant-pod` does NOT exist (rejected by admission controller)
- [ ] Error from rejected pod is documented in `/tmp/violation.txt`
- [ ] `/tmp/violation.txt` contains the PSS violation message
