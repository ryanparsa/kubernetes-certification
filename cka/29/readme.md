# Question 12 | Schedule Pod on Controlplane Nodes

Create a *Pod* of image `httpd:2-alpine` in *Namespace* `default`.

The *Pod* should be named `pod1` and the container should be named `pod1-container`.

This *Pod* should only be scheduled on controlplane nodes.

Do not add new labels to any nodes.

## Answer

First we find the controlplane node(s) and their taints:

```bash
k get node
NAME                        STATUS   ROLES           AGE   VERSION
cka-lab-control-plane       Ready    control-plane   90m   v1.33.1
cka-lab-worker              Ready    <none>          85m   v1.33.1

k describe node cka-lab-control-plane | grep Taint -A1
Taints:             node-role.kubernetes.io/control-plane:NoSchedule
Unschedulable:      false

k get node cka-lab-control-plane --show-labels
NAME                    STATUS   ROLES           AGE   VERSION   LABELS
cka-lab-control-plane   Ready    control-plane   91m   v1.33.1   beta.kubernetes.io/arch=amd64,...,node-role.kubernetes.io/control-plane=,...
```

Next we create the *Pod* yaml:

```bash
k run pod1 --image=httpd:2-alpine --dry-run=client -o yaml > 12.yaml
```

### Solution using NodeSelector

Use the K8s docs and search for tolerations and nodeSelector to find examples, then update:

```yaml
# 12.yaml
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

Important here to add the toleration for running on controlplane nodes, but also the `nodeSelector` to make sure it only runs on controlplane nodes. If we just specify a toleration the *Pod* can be scheduled on controlplane or worker nodes.

### Solution using NodeAffinity

We could also use `nodeAffinity` instead of `nodeSelector`, although in this case it is more complex and not really suggested:

```yaml
# 12.yaml
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
k -f 12.yaml create
pod/pod1 created

k get pod pod1 -o wide
NAME   READY   STATUS    ...   NODE                          NOMINATED NODE   READINESS GATES
pod1   1/1     Running   ...   cka-lab-control-plane         <none>           <none>
```

We can see the *Pod* is scheduled on the controlplane node.
