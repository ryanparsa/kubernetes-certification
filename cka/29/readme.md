# Question 29 | Schedule Pod on Controlplane Nodes

> **Solve this question on:** the "cka-lab-29" kind cluster

Create a *Pod* of image `httpd:2-alpine` in *Namespace* `default`.

The *Pod* should be named `pod1` and the *Container* should be named `pod1-container`.

This *Pod* should only be scheduled on *Controlplane Nodes*.

Do not add new labels to any *Nodes*.

## Answer

First we find the *Controlplane Node(s)* and their taints:

```bash
kubectl get node
NAME                           STATUS   ROLES           AGE   VERSION
cka-lab-29-control-plane       Ready    control-plane   90m   v1.33.1
cka-lab-29-worker              Ready    <none>          85m   v1.33.1

kubectl describe node cka-lab-29-control-plane | grep Taint -A1
Taints:             node-role.kubernetes.io/control-plane:NoSchedule
Unschedulable:      false

kubectl get node cka-lab-29-control-plane --show-labels
NAME                       STATUS   ROLES           AGE   VERSION   LABELS
cka-lab-29-control-plane   Ready    control-plane   91m   v1.33.1   beta.kubernetes.io/arch=amd64,...,node-role.kubernetes.io/control-plane=,...
```

Next we create the *Pod* yaml:

```bash
kubectl run pod1 --image=httpd:2-alpine --dry-run=client -o yaml > cka/29/course/29.yaml
```

### Solution using NodeSelector

Use the *Kubernetes* docs and search for tolerations and `nodeSelector` to find examples, then update:

```yaml
# cka/29/course/29.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: pod1
  name: pod1
spec:
  containers:
  - image: httpd:2-alpine
    name: pod1-container                       # change
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
  tolerations:                                 # add
  - effect: NoSchedule                         # add
    key: node-role.kubernetes.io/control-plane # add
  nodeSelector:                                # add
    node-role.kubernetes.io/control-plane: ""  # add
status: {}
```

> [!NOTE]
> ℹ️ The `nodeSelector` specifies `node-role.kubernetes.io/control-plane` with no value because this is a key-only label and we want to match regardless of the value

Important here to add the toleration for running on *Controlplane Nodes*, but also the `nodeSelector` to make sure it only runs on *Controlplane Nodes*. If we just specify a toleration the *Pod* can be scheduled on *Controlplane* or *Worker Nodes*.

### Solution using NodeAffinity

We could also use `nodeAffinity` instead of `nodeSelector`, although in this case it is more complex and not really suggested:

```yaml
# cka/29/course/29.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: pod1
  name: pod1
spec:
  containers:
  - image: httpd:2-alpine
    name: pod1-container                       # change
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
  tolerations:                                 # add
  - effect: NoSchedule                         # add
    key: node-role.kubernetes.io/control-plane # add
  affinity:                                            # add
    nodeAffinity:                                      # add
      requiredDuringSchedulingIgnoredDuringExecution:  # add
        nodeSelectorTerms:                             # add
        - matchExpressions:                            # add
          - key: node-role.kubernetes.io/control-plane # add
            operator: Exists                           # add
status: {}
```

Using `nodeAffinity` still requires the toleration.

### Verify

Now we create the *Pod* and and check if is scheduled:

```bash
kubectl create -f cka/29/course/29.yaml
pod/pod1 created

kubectl get pod pod1 -o wide
NAME   READY   STATUS    ...   NODE                             NOMINATED NODE   READINESS GATES
pod1   1/1     Running   ...   cka-lab-29-control-plane         <none>           <none>
```

We can see the *Pod* is scheduled on the *Controlplane Node*.


## Checklist (Score: 0/6)

- [ ] *Pod* is running
- [ ] *Pod* has single *Container*
- [ ] *Container* has correct name
- [ ] *Container* has correct image
- [ ] *Pod* is scheduled on *Controlplane*
- [ ] *Pod* will only be scheduled on *Controlplane Nodes*
