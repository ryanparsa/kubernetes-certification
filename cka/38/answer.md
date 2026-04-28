## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/pods/

### Create the namespace

```bash
kubectl create namespace app-team1
```

### Create the pod

```bash
kubectl run nginx-pod --image=nginx:1.19 -n app-team1 --labels=run=nginx-pod
```

### Verify

```bash
kubectl get pod nginx-pod -n app-team1 --show-labels
```

## Checklist (Score: 0/5)

- [ ] Namespace `app-team1` exists
- [ ] Pod `nginx-pod` exists in namespace `app-team1`
- [ ] Pod uses image `nginx:1.19`
- [ ] Pod has label `run=nginx-pod`
- [ ] Pod is in Running state
