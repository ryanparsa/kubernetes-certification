## Answer

**Reference:** https://kubernetes.io/docs/concepts/storage/storage-classes/

### Create the StorageClass

```yaml
# lab/fast-storage.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```

```bash
kubectl apply -f lab/fast-storage.yaml
```

### Verify

```bash
kubectl get storageclass fast-storage
kubectl describe storageclass fast-storage
```

## Checklist (Score: 0/3)

- [ ] StorageClass `fast-storage` exists
- [ ] StorageClass uses provisioner `kubernetes.io/no-provisioner`
- [ ] StorageClass has `volumeBindingMode: WaitForFirstConsumer`
