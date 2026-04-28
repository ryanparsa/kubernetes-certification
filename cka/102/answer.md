## Answer

**Reference:** https://kubernetes.io/docs/reference/kubectl/generated/kubectl_scale/

### Identify the resource

List the *Pods* in the namespace:

```bash
kubectl -n project-c13 get pods
```

Check what controller manages these *Pods*:

```bash
kubectl -n project-c13 get deploy,sts,ds
```

The output shows that `o3db` is a *StatefulSet*.

### Scale the StatefulSet

Scale the *StatefulSet* to 1 replica:

```bash
kubectl -n project-c13 scale sts o3db --replicas 1
```

Verify the change:

```bash
kubectl -n project-c13 get sts o3db
```

## Checklist (Score: 0/2)

- [ ] StatefulSet `o3db` in namespace `project-c13` has `replicas: 1`
- [ ] StatefulSet `o3db` in namespace `project-c13` has 1 ready replica
