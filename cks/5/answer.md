## Answer

**Reference:** https://kubernetes.io/docs/concepts/storage/volumes/#hostpath

### Create the namespace

```bash
kubectl create namespace binary-verify
```

### Create the pod with hostPath volume

```yaml
# lab/verify-bin.yaml
apiVersion: v1
kind: Pod
metadata:
  name: verify-bin
  namespace: binary-verify
spec:
  containers:
  - name: busybox
    image: busybox
    command: ["/bin/sh", "-c"]
    args:
    - |
      sha256sum /host-bin/kubectl >> /tmp/verified-hashes.txt
      sha256sum /host-bin/kubelet >> /tmp/verified-hashes.txt
      sleep 3600
    volumeMounts:
    - name: host-bin
      mountPath: /host-bin
      readOnly: true
  volumes:
  - name: host-bin
    hostPath:
      path: /usr/bin
      type: Directory
```

```bash
kubectl apply -f lab/verify-bin.yaml
kubectl wait pod verify-bin -n binary-verify --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl get pod verify-bin -n binary-verify
kubectl exec verify-bin -n binary-verify -- cat /tmp/verified-hashes.txt
```

The output should show SHA256 hashes for the `kubectl` and `kubelet` binaries.

> [!NOTE]
> This lab uses a `hostPath` volume which mounts files directly from the node filesystem. In production, ensure strict RBAC controls prevent unauthorized use of `hostPath` volumes.

## Checklist (Score: 0/5)

- [ ] Pod `verify-bin` exists in namespace `binary-verify`
- [ ] Pod mounts host `/usr/bin` at `/host-bin` as read-only
- [ ] Volume uses `hostPath` type `Directory`
- [ ] Pod command calculates SHA256 of `/host-bin/kubectl` into `/tmp/verified-hashes.txt`
- [ ] Pod command calculates SHA256 of `/host-bin/kubelet` into `/tmp/verified-hashes.txt`
