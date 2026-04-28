## Answer

**Reference:** https://kubernetes.io/docs/concepts/storage/storage-classes/

### Create the new StorageClass

```yaml
# lab/49-sc.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-local
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: rancher.io/local-path
volumeBindingMode: WaitForFirstConsumer
```

```bash
kubectl apply -f lab/49-sc.yaml
```

### Remove default annotation from existing default StorageClass(es)

First, identify any existing default StorageClasses:

```bash
kubectl get storageclass
```

Then remove the default annotation from each one (replace `<name>` with the actual class name):

```bash
kubectl patch storageclass <name> -p '{"metadata": {"annotations": {"storageclass.kubernetes.io/is-default-class": "false"}}}'
```

### Verify

```bash
kubectl get storageclass
# fast-local should show (default)
```

## Checklist (Score: 0/4)

- [ ] StorageClass `fast-local` exists
- [ ] Provisioner is `rancher.io/local-path`
- [ ] VolumeBindingMode is `WaitForFirstConsumer`
- [ ] `fast-local` is the only default StorageClass
