# Kubernetes Scheduling Reference

Reference for how the scheduler places pods onto nodes: node selectors, affinity,
taints/tolerations, manual scheduling, PriorityClasses, topology spread, and DaemonSets.

---

## 1. Scheduling Pipeline

```
1. Filtering (Predicates)
   - NodeSelector / nodeAffinity
   - TaintToleration
   - ResourceFit (requests vs. allocatable)
   - PodTopologySpread
   - ...

2. Scoring (Priorities)
   - LeastAllocated (spread pods evenly)
   - NodeAffinity (preferred rules)
   - PodAffinity / PodAntiAffinity
   - ImageLocality (prefer nodes with image cached)
   - ...

3. Binding
   - Scheduler writes spec.nodeName on the Pod
   - kubelet on that node picks it up and starts the containers
```

---

## 2. nodeName (Direct Assignment)

Bypasses the scheduler entirely. Pod is placed on the named node unconditionally.

```yaml
spec:
  nodeName: worker-1
  containers:
  - name: app
    image: nginx
```

> Use for manual scheduling (e.g. when kube-scheduler is stopped) or for debugging.
> Not recommended in production — the scheduler's resource checks are bypassed.

---

## 3. nodeSelector

Simplest affinity mechanism. Pod is only scheduled on nodes whose labels match ALL
key/value pairs.

```yaml
spec:
  nodeSelector:
    disktype: ssd
    kubernetes.io/os: linux
  containers:
  - name: app
    image: nginx
```

```bash
# Label a node
kubectl label node worker-1 disktype=ssd

# Remove a label
kubectl label node worker-1 disktype-
```

---

## 4. Node Affinity

More expressive than `nodeSelector`. Supports `In`, `NotIn`, `Exists`, `DoesNotExist`,
`Gt`, `Lt` operators.

### Required (hard rule — pod not scheduled if not met)

```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd
            - nvme
```

### Preferred (soft rule — scheduler tries but doesn't guarantee)

```yaml
spec:
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 80                    # higher weight = stronger preference (1-100)
        preference:
          matchExpressions:
          - key: region
            operator: In
            values:
            - us-east-1
      - weight: 20
        preference:
          matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd
```

> `IgnoredDuringExecution` — already-running pods are NOT evicted if the node labels change.

---

## 5. Pod Affinity and Anti-Affinity

Schedules pods relative to **other pods** (co-location or spread).

### Pod Affinity — place with matching pods

```yaml
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app: cache          # schedule near pods with app=cache
        topologyKey: kubernetes.io/hostname
```

### Pod Anti-Affinity — avoid nodes with matching pods

```yaml
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app: frontend       # don't schedule on same node as other frontend pods
        topologyKey: kubernetes.io/hostname
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchLabels:
              app: frontend
          topologyKey: topology.kubernetes.io/zone    # spread across zones
```

> `topologyKey` groups nodes by a label. Common values:
> - `kubernetes.io/hostname` — node-level
> - `topology.kubernetes.io/zone` — availability zone
> - `topology.kubernetes.io/region` — region

---

## 6. Taints and Tolerations

**Taints** repel pods from nodes. **Tolerations** allow pods to be scheduled despite a taint.

### Taint effects

| Effect | Meaning |
|---|---|
| `NoSchedule` | New pods without a matching toleration won't be scheduled |
| `PreferNoSchedule` | Scheduler tries to avoid placing pods here; not guaranteed |
| `NoExecute` | Existing pods without toleration are evicted; new pods also blocked |

### Managing taints

```bash
# Taint a node
kubectl taint node worker-1 gpu=true:NoSchedule

# Taint with NoExecute (evicts existing pods too)
kubectl taint node worker-1 maintenance=:NoExecute

# Remove a taint (append -)
kubectl taint node worker-1 gpu=true:NoSchedule-

# View taints on a node
kubectl describe node worker-1 | grep Taints
```

### Toleration in a Pod spec

```yaml
spec:
  tolerations:
  - key: gpu
    operator: Equal
    value: "true"
    effect: NoSchedule
  - key: node-role.kubernetes.io/control-plane
    operator: Exists            # matches any value
    effect: NoSchedule
  - key: maintenance
    operator: Exists
    effect: NoExecute
    tolerationSeconds: 300      # stay for 5min then evict
```

### Control plane taint

`kubeadm` adds `node-role.kubernetes.io/control-plane:NoSchedule` to control-plane
nodes. To schedule user workloads on the control plane, add a matching toleration or
remove the taint:

```bash
# Remove control-plane taint (single-node cluster)
kubectl taint node <node> node-role.kubernetes.io/control-plane:NoSchedule-
```

---

## 7. Manual Scheduling (when kube-scheduler is stopped)

When the scheduler is down, pods remain `Pending`. Assign them manually:

```bash
# Stop the scheduler (move manifest out of watched dir)
mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/kube-scheduler.yaml

# Manually schedule a pod by setting nodeName via a Binding object
kubectl apply -f - <<EOF
apiVersion: v1
kind: Binding
metadata:
  name: my-pod
  namespace: default
target:
  apiVersion: v1
  kind: Node
  name: worker-1
EOF

# Or: patch the pod's nodeName directly
kubectl patch pod my-pod -p '{"spec":{"nodeName":"worker-1"}}'

# Restart the scheduler
mv /tmp/kube-scheduler.yaml /etc/kubernetes/manifests/kube-scheduler.yaml
```

---

## 8. PriorityClass

Determines the scheduling order and eviction priority for pods.

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000            # higher number = higher priority
globalDefault: false
preemptionPolicy: PreemptLowerPriority   # default
description: "Critical workloads"
```

```yaml
spec:
  priorityClassName: high-priority
  containers:
  - name: app
    image: nginx
```

Built-in classes:
- `system-cluster-critical` (2000000000) — used by CoreDNS, kube-dns
- `system-node-critical` (2000001000) — used by kube-proxy, metrics-server

---

## 9. TopologySpreadConstraints

Spreads pods evenly across topology domains (nodes, zones).

```yaml
spec:
  topologySpreadConstraints:
  - maxSkew: 1                          # max difference in pod count between domains
    topologyKey: kubernetes.io/hostname
    whenUnsatisfiable: DoNotSchedule    # or ScheduleAnyway
    labelSelector:
      matchLabels:
        app: my-app
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: ScheduleAnyway
    labelSelector:
      matchLabels:
        app: my-app
```

> `maxSkew: 1` means no domain can have more than 1 extra pod compared to the least-loaded domain.

---

## 10. DaemonSet Scheduling

A DaemonSet ensures exactly one pod per node (or per matching node). It bypasses the
default scheduler for node placement — it uses its own controller.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-system
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane   # run on control-plane too
        operator: Exists
        effect: NoSchedule
      nodeSelector:
        kubernetes.io/os: linux       # optional: limit to Linux nodes
      containers:
      - name: fluentd
        image: fluent/fluentd:v1.16
```

DaemonSet pods on tainted nodes (e.g. control-plane) require matching tolerations.

---

## 11. Deployment on All Nodes

A DaemonSet guarantees one-per-node. To run a Deployment on all nodes use:

```yaml
spec:
  replicas: <total node count>
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: my-app
            topologyKey: kubernetes.io/hostname
```

This prevents two replicas landing on the same node.

---

## 12. Useful Commands

```bash
# See why a pod is pending
kubectl describe pod my-pod | grep -A 10 Events

# List node labels
kubectl get nodes --show-labels
kubectl describe node worker-1 | grep Labels -A 20

# Check node allocatable resources vs requests
kubectl describe node worker-1 | grep -A 5 Allocatable

# Check which node a pod is on
kubectl get pod my-pod -o wide

# Cordon a node (prevent new pods)
kubectl cordon worker-1

# Drain a node (evict all pods + cordon)
kubectl drain worker-1 --ignore-daemonsets --delete-emptydir-data

# Uncordon a node
kubectl uncordon worker-1
```
