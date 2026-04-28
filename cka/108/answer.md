## Answer

**Reference:** <https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodename>

### 1. Stop the scheduler

To stop the scheduler, move its static *Pod* manifest out of the manifests directory.

```bash
docker exec cka-lab-108-control-plane mv /etc/kubernetes/manifests/kube-scheduler.yaml /etc/kubernetes/
```

### 2. Create the first Pod

```bash
kubectl run manual-schedule --image=httpd:2.4-alpine
```

Check its status:
```bash
kubectl get pod manual-schedule
```
It should be in `Pending` state.

### 3. Manually schedule the Pod

Export the *Pod* manifest, add `nodeName`, and replace the *Pod*.

```bash
kubectl get pod manual-schedule -o json | jq '.spec.nodeName="cka-lab-108-worker"' | kubectl replace --force -f -
```

### 4. Restart the scheduler

Move the manifest back.

```bash
docker exec cka-lab-108-control-plane mv /etc/kubernetes/kube-scheduler.yaml /etc/kubernetes/manifests/
```

### 5. Create the second Pod

```bash
kubectl run manual-schedule2 --image=httpd:2.4-alpine
```

Check its status:
```bash
kubectl get pod manual-schedule2 -o wide
```
It should be in `Running` state on `cka-lab-108-worker`.

## Checklist (Score: 0/3)

- [ ] *Pod* `manual-schedule` is running on `cka-lab-108-worker`.
- [ ] *Pod* `manual-schedule2` is running on `cka-lab-108-worker`.
- [ ] `kube-scheduler` is running correctly.
