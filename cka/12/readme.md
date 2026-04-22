# Question 12 | Deployment on all Nodes

Implement the following in *Namespace* `project-tiger`:

- Create a *Deployment* named `deploy-important` with `3` replicas
- The *Deployment* and its *Pods* should have label `id=very-important`
- First container named `container1` with image `nginx:1-alpine`
- Second container named `container2` with image `google/pause`
- There should only ever be **one** *Pod* of that *Deployment* running on **one** worker node, use `topologyKey: kubernetes.io/hostname` for this

> ℹ️ Because there are two worker nodes and the *Deployment* has three replicas the result should be that the third *Pod* won't be scheduled. In a way this scenario simulates the behaviour of a *DaemonSet*, but using a *Deployment* with a fixed number of replicas

## Answer

There are two possible ways, one using `podAntiAffinity` and one using `topologySpreadConstraint`.

### PodAntiAffinity

The idea here is that we create a "Inter-pod anti-affinity" which allows us to say a *Pod* should only be scheduled on a node where another *Pod* of a specific label (here the same label) is not already running.

Let's begin by creating the *Deployment* template:

```bash
k -n project-tiger create deployment --image=nginx:1-alpine deploy-important --dry-run=client -o yaml > 12.yaml
```

Then change the yaml to:

```yaml
# 12.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    id: very-important          # change
  name: deploy-important
  namespace: project-tiger      # important
spec:
  replicas: 3                   # change
  selector:
    matchLabels:
      id: very-important        # change
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        id: very-important      # change
    spec:
      containers:
      - image: nginx:1-alpine
        name: container1        # change
        resources: {}
      - image: google/pause     # add
        name: container2        # add
      affinity:                                     # add
        podAntiAffinity:                            # add
          requiredDuringSchedulingIgnoredDuringExecution: # add
          - labelSelector:                          # add
              matchExpressions:                     # add
              - key: id                             # add
                operator: In                        # add
                values:                             # add
                - very-important                    # add
            topologyKey: kubernetes.io/hostname     # add
status: {}
```

Specify a topologyKey, which is a pre-populated Kubernetes label, you can find this by describing a node.

### TopologySpreadConstraints

We can achieve the same with `topologySpreadConstraints`. Best to try out and play with both.

```yaml
# 12.yaml (topologySpreadConstraints version)
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    id: very-important          # change
  name: deploy-important
  namespace: project-tiger      # important
spec:
  replicas: 3                   # change
  selector:
    matchLabels:
      id: very-important        # change
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        id: very-important      # change
    spec:
      containers:
      - image: nginx:1-alpine
        name: container1        # change
        resources: {}
      - image: google/pause     # add
        name: container2        # add
      topologySpreadConstraints:                 # add
      - maxSkew: 1                               # add
        topologyKey: kubernetes.io/hostname      # add
        whenUnsatisfiable: DoNotSchedule         # add
        labelSelector:                           # add
          matchLabels:                           # add
            id: very-important                   # add
status: {}
```

### Apply and Run

Let's run it:

```bash
k -f 12.yaml create
deployment.apps/deploy-important created
```

Then we check the *Deployment* status where it shows 2/3 ready count:

```bash
k -n project-tiger get deploy -l id=very-important
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
deploy-important   2/3     3            2           19s
```

And running the following we see one *Pod* on each worker node and one not scheduled.

```bash
k -n project-tiger get pod -o wide -l id=very-important
NAME                                  READY   STATUS    ...   IP           NODE
deploy-important-78f98b75f9-5s6js   0/2     Pending  ...   <none>       <none>
deploy-important-78f98b75f9-657hx   2/2     Running  ...   10.244.1.x   cka-lab-worker
deploy-important-78f98b75f9-9bz8q   2/2     Running  ...   10.244.2.x   cka-lab-worker2
```

If we kubectl describe the not scheduled *Pod* it will show us the reason `didn't match pod anti-affinity rules`:

```text
Warning  FailedScheduling  119s (x2 over 2m1s)  default-scheduler  0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 2 node(s) didn't match pod anti-affinity rules. preemption: 0/3 nodes are available: 1 Preemption is not helpful for scheduling, 2 No preemption victims found for incoming pod.
```

Or our topologySpreadConstraints reason `didn't match pod topology spread constraints`:

```text
Warning  FailedScheduling  20s (x2 over 22s)  default-scheduler  0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 2 node(s) didn't match pod topology spread constraints. preemption: 0/3 nodes are available: 1 Preemption is not helpful for scheduling, 2 No preemption victims found for incoming pod.
```
