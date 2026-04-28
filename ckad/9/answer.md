## Answer

**Reference:** https://kubernetes.io/docs/tasks/configure-pod-container/security-context/

### Create namespace and ServiceAccount

```bash
kubectl create namespace secure
kubectl create serviceaccount app-sa -n secure
kubectl get serviceaccount app-sa -n secure
```

### Create the secure-pod manifest

```yaml
# lab/secure-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
  namespace: secure
spec:
  serviceAccountName: app-sa
  securityContext:
    runAsUser: 1000
  containers:
  - name: nginx
    image: nginx
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        add:
        - NET_ADMIN
```

```bash
kubectl apply -f lab/secure-pod.yaml
kubectl get pod secure-pod -n secure
```

### Verify the security context

```bash
# Confirm running user is 1000
kubectl exec secure-pod -n secure -- id

# Confirm pod spec
kubectl get pod secure-pod -n secure -o jsonpath='{.spec.securityContext}'
kubectl get pod secure-pod -n secure -o jsonpath='{.spec.containers[0].securityContext}'

# Confirm ServiceAccount
kubectl get pod secure-pod -n secure -o jsonpath='{.spec.serviceAccountName}'
```

## Checklist (Score: 0/5)

- [ ] Namespace `secure` exists and ServiceAccount `app-sa` created in it
- [ ] Pod `secure-pod` uses ServiceAccount `app-sa`
- [ ] Pod runs as user ID `1000` (`spec.securityContext.runAsUser`)
- [ ] Container has capability `NET_ADMIN` added
- [ ] Container has `allowPrivilegeEscalation: false`
