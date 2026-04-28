## Answer

**Reference:** https://kubernetes.io/docs/concepts/storage/persistent-volumes/

### Create the namespace

```bash
kubectl create namespace manual-storage
```

### Create the PersistentVolume

```yaml
# lab/50-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: manual-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /mnt/data
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - k3d-cluster-agent-0
```

```bash
kubectl apply -f lab/50-pv.yaml
```

### Create the PVC

```yaml
# lab/50-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: manual-pvc
  namespace: manual-storage
spec:
  storageClassName: ""
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

```bash
kubectl apply -f lab/50-pvc.yaml
```

### Create the Pod

```yaml
# lab/50-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: manual-pod
  namespace: manual-storage
spec:
  containers:
  - name: busybox
    image: busybox
    command: ["sleep", "3600"]
    volumeMounts:
    - name: data
      mountPath: /data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: manual-pvc
```

```bash
kubectl apply -f lab/50-pod.yaml
kubectl wait pod manual-pod -n manual-storage --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl get pv manual-pv
kubectl get pvc manual-pvc -n manual-storage
kubectl get pod manual-pod -n manual-storage
```

## Checklist (Score: 0/6)

- [ ] PersistentVolume `manual-pv` exists with `1Gi` storage
- [ ] PV uses hostPath `/mnt/data` with node affinity to `k3d-cluster-agent-0`
- [ ] PVC `manual-pvc` exists in `manual-storage` namespace
- [ ] PVC binds to `manual-pv`
- [ ] Pod `manual-pod` exists in `manual-storage` namespace
- [ ] Pod mounts the PVC at `/data` and runs `sleep 3600`
