## Answer

**Reference:** https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/

### Create the namespace

```bash
kubectl create namespace scheduling
```

### Create PriorityClasses and Pods with anti-affinity

```yaml
# lab/66-priority.yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
globalDefault: false
description: "High priority workloads"
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 100
globalDefault: false
description: "Low priority workloads"
---
apiVersion: v1
kind: Pod
metadata:
  name: high-priority
  namespace: scheduling
  labels:
    priority: high
spec:
  priorityClassName: high-priority
  containers:
  - name: nginx
    image: nginx
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: priority
            operator: In
            values:
            - high
            - low
        topologyKey: kubernetes.io/hostname
---
apiVersion: v1
kind: Pod
metadata:
  name: low-priority
  namespace: scheduling
  labels:
    priority: low
spec:
  priorityClassName: low-priority
  containers:
  - name: nginx
    image: nginx
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: priority
            operator: In
            values:
            - high
            - low
        topologyKey: kubernetes.io/hostname
```

```bash
kubectl apply -f lab/66-priority.yaml
kubectl wait pod high-priority low-priority -n scheduling --for=condition=Ready --timeout=60s
```

### Verify

```bash
kubectl get pods -n scheduling -o wide
# high-priority and low-priority pods should be on different nodes
kubectl get priorityclass
```

## Checklist (Score: 0/6)

- [ ] PriorityClass `high-priority` exists with value `1000`
- [ ] PriorityClass `low-priority` exists with value `100`
- [ ] Pod `high-priority` exists in `scheduling` namespace using `high-priority` PriorityClass
- [ ] Pod `low-priority` exists in `scheduling` namespace using `low-priority` PriorityClass
- [ ] Both pods have `podAntiAffinity` configured with `requiredDuringSchedulingIgnoredDuringExecution`
- [ ] Pods are scheduled on different nodes
