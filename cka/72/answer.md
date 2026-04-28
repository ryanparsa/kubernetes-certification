## Answer

**Reference:** https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodename

### Manually schedule the Pod

Since the *Controlplane Node* is tainted and we are not allowed to add *Tolerations*, we must bypass the *Scheduler* by specifying the `nodeName` field in the *Pod* spec.

First, find the name of the *Controlplane Node*:

```bash
kubectl get node
```

Create the *Pod* manifest:

```bash
# kubectl run pod --image=httpd:2.4.41-alpine --dry-run=client -o yaml > cka/72/lab/72.yaml
```

Update the manifest to include `nodeName` and the correct container name:

```yaml
# cka/72/lab/72.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod
spec:
  nodeName: cka-lab-72-control-plane # Manually schedule on controlplane
  containers:
  - name: pod-container
    image: httpd:2.4.41-alpine
```

Apply the manifest:

```bash
kubectl apply -f cka/72/lab/72.yaml
```

Verify the *Pod* is running on the *Controlplane Node*:

```bash
kubectl get pod pod -o wide
```

## Checklist (Score: 0/5)

- [ ] *Pod* named `pod` created in `default` *Namespace*
- [ ] *Container* named `pod-container`
- [ ] *Container* image is `httpd:2.4.41-alpine`
- [ ] *Pod* is scheduled on the *Controlplane Node*
- [ ] *Pod* spec does not contain any *Tolerations*
