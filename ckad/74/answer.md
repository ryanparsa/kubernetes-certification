## Answer

**Reference:** <https://kubernetes.io/docs/tasks/configure-pod-container/security-context/>

### Create the Pod manifest

```bash
kubectl run secured --image=nginx --dry-run=client -o yaml > lab/secured.yaml
```

Edit `lab/secured.yaml` to add the security context, volume and volume mount:

```yaml
# lab/secured.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: secured
  name: secured
spec:
  securityContext:
    fsGroup: 3000
  containers:
  - image: nginx
    name: secured
    volumeMounts:
    - name: data-vol
      mountPath: /data/app
    resources: {}
  volumes:
  - name: data-vol
    emptyDir: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
```

```bash
kubectl apply -f lab/secured.yaml
kubectl wait pod/secured --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl exec secured -- sh -c 'touch /data/app/logs.txt && ls -l /data/app'
# -rw-r--r-- 1 root 3000 0 ... logs.txt
```

The group ID `3000` confirms the `fsGroup` security context is applied.

## Checklist (Score: 0/4)

- [ ] Pod `secured` is running
- [ ] Pod has an `emptyDir` volume mounted at `/data/app`
- [ ] Pod-level `securityContext.fsGroup` is set to `3000`
- [ ] Files created in `/data/app` are owned by group `3000`
