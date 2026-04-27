# kubectl Output Formatting Reference — 4. `-o jsonpath`

> Part of [kubectl Output Formatting Reference](../kubectl Output Formatting.md)


JSONPath selects fields from the JSON representation of the resource.

### Basic field access

```bash
# Get the ClusterIP of a service
kubectl get svc kubernetes -o jsonpath='{.spec.clusterIP}'

# Get the node name a pod is scheduled on
kubectl get pod my-pod -o jsonpath='{.spec.nodeName}'

# Get all container images in a pod
kubectl get pod my-pod -o jsonpath='{.spec.containers[*].image}'

# Get pod IP
kubectl get pod my-pod -o jsonpath='{.status.podIP}'

# Get a node's internal IP
kubectl get node worker-1 -o jsonpath=\
'{.status.addresses[?(@.type=="InternalIP")].address}'
```

### Iterating lists

```bash
# All pod names in a namespace
kubectl get pods -n kube-system \
  -o jsonpath='{.items[*].metadata.name}'

# Each pod on its own line
kubectl get pods -A \
  -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\n"}{end}'

# All container images across all pods
kubectl get pods -A \
  -o jsonpath='{range .items[*]}{range .spec.containers[*]}{.image}{"\n"}{end}{end}'
```

### Filtering with `?(@.field==value)`

```bash
# Get the InternalIP of all nodes
kubectl get nodes -o jsonpath=\
'{range .items[*]}{.metadata.name}{"\t"}{.status.addresses[?(@.type=="InternalIP")].address}{"\n"}{end}'

# Get only Ready nodes
kubectl get nodes -o jsonpath=\
'{range .items[*]}{.metadata.name}{"\t"}{.status.conditions[?(@.type=="Ready")].status}{"\n"}{end}'
```

### Common field paths

| Object | Field | JSONPath |
|---|---|---|
| Pod | Node name | `.spec.nodeName` |
| Pod | Pod IP | `.status.podIP` |
| Pod | Restart count | `.status.containerStatuses[0].restartCount` |
| Pod | QoS class | `.status.qosClass` |
| Pod | Creation time | `.metadata.creationTimestamp` |
| Pod | Labels | `.metadata.labels` |
| Node | Internal IP | `.status.addresses[?(@.type=="InternalIP")].address` |
| Node | Allocatable CPU | `.status.allocatable.cpu` |
| Node | Allocatable memory | `.status.allocatable.memory` |
| Node | OS image | `.status.nodeInfo.osImage` |
| Node | Kernel version | `.status.nodeInfo.kernelVersion` |
| Node | Container runtime | `.status.nodeInfo.containerRuntimeVersion` |
| Event | Reason | `.reason` |
| Event | Message | `.message` |
| Event | Involved object | `.involvedObject.name` |
| Service | ClusterIP | `.spec.clusterIP` |
| Service | Ports | `.spec.ports[*].port` |

---

