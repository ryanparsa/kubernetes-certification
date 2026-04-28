## Answer

**Reference:** <https://kubernetes.io/docs/concepts/configuration/secret/>

### Create the Namespace

```bash
kubectl create namespace meerkat
```

### Investigate the broken Deployment

```bash
kubectl get deployment meerkat -n meerkat
kubectl describe deployment meerkat -n meerkat
kubectl get pods -n meerkat
kubectl describe pod <pod-name> -n meerkat
# Look for image pull errors or wrong image
```

### Fix the Deployment image

```bash
kubectl set image deployment/meerkat <container>=<correct-image> -n meerkat
kubectl rollout status deployment/meerkat -n meerkat
```

### Create the Secret

```bash
kubectl create secret generic meerkat \
  --from-literal=key=value \
  -n meerkat
```

### Verify

```bash
kubectl get secrets -n meerkat
kubectl get deployment meerkat -n meerkat
kubectl get pods -n meerkat
```

## Checklist (Score: 0/4)

- [ ] Namespace `meerkat` exists
- [ ] Secret `meerkat-secret` accessible only within Namespace `meerkat`
- [ ] Deployment `meerkat` fixed and running with correct image
- [ ] Secret `meerkat` created in Namespace `meerkat`
