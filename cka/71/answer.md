## Answer

**Reference:** <https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/>

### Create the DaemonSet

Generate a base deployment manifest and convert it to a DaemonSet:

```bash
kubectl create deploy nginx-ds --image=nginx --dry-run=client -o yaml > lab/nginx-ds.yaml
```

Edit to convert Deployment -> DaemonSet (remove `replicas` and `strategy`, change `kind`):

```yaml
# lab/nginx-ds.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  labels:
    app: nginx-ds
  name: nginx-ds
spec:
  selector:
    matchLabels:
      app: nginx-ds
  template:
    metadata:
      labels:
        app: nginx-ds
    spec:
      containers:
      - image: nginx
        name: nginx
```

```bash
kubectl apply -f lab/nginx-ds.yaml
```

### Verify

```bash
kubectl get daemonset nginx-ds
# NAME       DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
# nginx-ds   2         2         2       2            2           <none>          20s

kubectl get pods -l app=nginx-ds -o wide
# NAME             READY   STATUS    ...   NODE
# nginx-ds-xxxxx   1/1     Running   ...   cka-lab-71-control-plane
# nginx-ds-yyyyy   1/1     Running   ...   cka-lab-71-worker
```

One pod per node -- the DaemonSet does not add tolerations, so it respects existing taints (e.g. the control-plane NoSchedule taint may prevent scheduling there unless tolerated).

## Checklist (Score: 0/4)

- [ ] DaemonSet `nginx-ds` exists using the `nginx` image
- [ ] DaemonSet uses the correct label selector `app=nginx-ds`
- [ ] One pod per schedulable node is running
- [ ] No new taints were added to any nodes
