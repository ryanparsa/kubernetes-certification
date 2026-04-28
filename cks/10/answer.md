## Answer

**Reference:** https://kubernetes.io/docs/tutorials/security/seccomp/

### Create the namespace

```bash
kubectl create namespace seccomp-profile
```

### Create the pod with seccomp profile

```yaml
# lab/seccomp-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: seccomp-pod
  namespace: seccomp-profile
spec:
  securityContext:
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: nginx
    image: nginx
```

```bash
kubectl apply -f lab/seccomp-pod.yaml
kubectl wait pod seccomp-pod -n seccomp-profile --for=condition=Ready --timeout=60s
```

### Create the ConfigMap with a custom seccomp profile

```yaml
# lab/seccomp-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: seccomp-config
  namespace: seccomp-profile
data:
  profile.json: |
    {
      "defaultAction": "SCMP_ACT_ERRNO",
      "architectures": ["SCMP_ARCH_X86_64"],
      "syscalls": [
        {
          "names": ["exit", "exit_group", "rt_sigreturn", "read", "write", "open"],
          "action": "SCMP_ACT_ALLOW"
        }
      ]
    }
```

```bash
kubectl apply -f lab/seccomp-config.yaml
```

### Verify

```bash
kubectl get pod seccomp-pod -n seccomp-profile -o jsonpath='{.spec.securityContext.seccompProfile}'
# should output: {"type":"RuntimeDefault"}

kubectl get configmap seccomp-config -n seccomp-profile -o jsonpath='{.data.profile\.json}'
```

## Checklist (Score: 0/5)

- [ ] Pod `seccomp-pod` exists in namespace `seccomp-profile`
- [ ] Pod has seccomp profile of type `RuntimeDefault`
- [ ] ConfigMap `seccomp-config` exists in namespace `seccomp-profile`
- [ ] ConfigMap has key `profile.json` with valid seccomp profile JSON
- [ ] Seccomp profile allows syscalls: `exit`, `exit_group`, `rt_sigreturn`, `read`, `write`, `open`
