## Answer

**Reference:** https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/

### Create the DaemonSet

```yaml
# lab/node-monitor.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-monitor
  namespace: default
  labels:
    app: node-monitor
spec:
  selector:
    matchLabels:
      app: node-monitor
  template:
    metadata:
      labels:
        app: node-monitor
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        operator: Exists
        effect: NoSchedule
      nodeSelector:
        kubernetes.io/os: linux
      containers:
      - name: monitor
        image: busybox
        command:
        - sh
        - -c
        - 'while true; do echo "Node: $(hostname)"; sleep 30; done'
        resources:
          requests:
            cpu: 50m
            memory: 32Mi
```

```bash
kubectl apply -f lab/node-monitor.yaml
kubectl rollout status daemonset/node-monitor --timeout=60s
```

### Verify

```bash
kubectl get daemonset node-monitor
# DESIRED should equal the number of nodes in the cluster

kubectl get pods -l app=node-monitor -o wide
# Each node should have exactly one Pod
```

### Key points

- Without the toleration for `node-role.kubernetes.io/control-plane`, the DaemonSet won't schedule a Pod on the control-plane node.
- `nodeSelector: kubernetes.io/os=linux` restricts the DaemonSet to Linux nodes only.

## Checklist (Score: 0/3)

- [ ] DaemonSet `node-monitor` in namespace `default` is created and all desired Pods are Running
- [ ] Toleration for `node-role.kubernetes.io/control-plane` is configured so control-plane nodes receive a Pod
- [ ] `nodeSelector: kubernetes.io/os=linux` and resource requests `cpu: 50m`, `memory: 32Mi` are set
