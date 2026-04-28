## Answer

**Reference:** <https://kubernetes.io/docs/tasks/run-application/configure-pdb/>

### Check current state of Deployments

```bash
kubectl get deployments -n sun
kubectl get pods -n sun
```

### Create PodDisruptionBudget for sun-1cc

```yaml
# lab/pdb-sun-1cc.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: pdb-sun-1cc
  namespace: sun
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: sun-1cc
```

### Create PodDisruptionBudget for sun-2cc

```yaml
# lab/pdb-sun-2cc.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: pdb-sun-2cc-deployment
  namespace: sun
spec:
  maxUnavailable: "40%"
  selector:
    matchLabels:
      app: sun-2cc
```

```bash
kubectl apply -f lab/pdb-sun-1cc.yaml
kubectl apply -f lab/pdb-sun-2cc.yaml
kubectl get pdb -n sun
```

## Checklist (Score: 0/4)

- [ ] PDB `pdb-sun-1cc` exists in Namespace `sun` with `minAvailable: 1`
- [ ] PDB `pdb-sun-2cc-deployment` exists in Namespace `sun` with `maxUnavailable: 40%`
- [ ] Both PDBs select the correct Deployments
- [ ] Deployments have `Available` replicas
