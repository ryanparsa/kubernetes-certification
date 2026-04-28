## Answer

**Reference:** <https://kubernetes.io/docs/concepts/workloads/pods/>

### Create Pod nemo-0

```yaml
# lab/nemo-0.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nemo-0
  namespace: nemo
  labels:
    id: nemo-0
spec:
  containers:
  - name: nemo-0
    image: nginx:1.14.2
    ports:
    - containerPort: 9090
      protocol: TCP
```

```bash
kubectl apply -f lab/nemo-0.yaml
```

### Find the node nemo-0 is running on

```bash
NODE=$(kubectl get pod nemo-0 -n nemo -o jsonpath='{.spec.nodeName}')
echo $NODE > /opt/course/22/node.txt
```

### Create Pod nemo-1 on the same node

```yaml
# lab/nemo-1.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nemo-1
  namespace: nemo
spec:
  nodeSelector:
    kubernetes.io/hostname: <node-name>
  containers:
  - name: nemo-1
    image: nginx:1.14.2
```

```bash
kubectl apply -f lab/nemo-1.yaml
kubectl get pods -n nemo -o wide
```

## Checklist (Score: 0/4)

- [ ] Pod `nemo-0` in Namespace `nemo` with label `id: nemo-0` and port 9090/TCP
- [ ] Node name written to `/opt/course/22/node.txt`
- [ ] Pod `nemo-1` in Namespace `nemo` using `nodeSelector` to land on same node as `nemo-0`
- [ ] Both Pods running with image `nginx:1.14.2`
