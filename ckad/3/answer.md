## Answer

**Reference:** https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

### Create three pods with label app=v1

```bash
kubectl run nginx1 --image=nginx --labels=app=v1
kubectl run nginx2 --image=nginx --labels=app=v1
kubectl run nginx3 --image=nginx --labels=app=v1
kubectl get pods --show-labels
```

### Change label of nginx2 to app=v2

```bash
kubectl label pod nginx2 app=v2 --overwrite
kubectl get pods --show-labels
```

### Add annotation owner=team-a to all pods with app=v1

After relabelling, `nginx1` and `nginx3` have `app=v1`. Target them with a label selector:

```bash
kubectl annotate pod -l app=v1 owner=team-a
kubectl describe pod nginx1 | grep owner
kubectl describe pod nginx3 | grep owner
```

### Create the scheduled pod with nodeSelector

```yaml
# lab/scheduled.yaml
apiVersion: v1
kind: Pod
metadata:
  name: scheduled
spec:
  nodeSelector:
    kubernetes.io/os: linux
  containers:
  - name: nginx
    image: nginx
```

```bash
kubectl apply -f lab/scheduled.yaml
kubectl get pod scheduled -o wide
```

### Verify

```bash
# nginx1 and nginx3 should have app=v1; nginx2 should have app=v2
kubectl get pods --show-labels

# Confirm annotation on app=v1 pods only
kubectl get pods -l app=v1 -o jsonpath='{range .items[*]}{.metadata.name}: {.metadata.annotations.owner}{"\n"}{end}'

# Confirm scheduled pod uses nodeSelector
kubectl get pod scheduled -o jsonpath='{.spec.nodeSelector}'
```

## Checklist (Score: 0/4)

- [ ] Pods `nginx1`, `nginx2`, `nginx3` all exist with original label `app=v1` (before relabelling)
- [ ] Pod `nginx2` has label `app=v2`
- [ ] Annotation `owner=team-a` added to all pods currently labelled `app=v1` (`nginx1` and `nginx3`)
- [ ] Pod `scheduled` uses `nodeSelector: kubernetes.io/os: linux`
