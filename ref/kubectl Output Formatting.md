# kubectl Output Formatting Reference

Reference for `kubectl` output modes: jsonpath, custom-columns, sort-by, wide, top,
and jq patterns for common Kubernetes objects.

---

## 1. Output Formats Overview

| Flag | What you get |
|---|---|
| `-o wide` | Extra columns (node, IP, nominated node, etc.) |
| `-o yaml` | Full resource as YAML |
| `-o json` | Full resource as JSON |
| `-o name` | Just `kind/name` — useful for scripting |
| `-o jsonpath='...'` | Extract specific fields with JSONPath |
| `-o jsonpath-file=file` | Read JSONPath expression from a file |
| `-o custom-columns=...` | Table with custom column definitions |
| `-o custom-columns-file=file` | Read column definitions from a file |
| `--sort-by=<field>` | Sort list output by a JSONPath field |
| `-o go-template=...` | Go template (rarely used in CKA) |

---

## 2. `-o wide`

```bash
kubectl get pods -o wide
# NAMESPACE  NAME     READY  STATUS   RESTARTS  AGE  IP           NODE       ...

kubectl get nodes -o wide
# NAME      STATUS  ROLES    AGE  VERSION  INTERNAL-IP  EXTERNAL-IP  OS-IMAGE  ...
```

---

## 3. `--sort-by`

`--sort-by` takes a JSONPath field expression. Applied to list output.

```bash
# Sort pods by creation time (oldest first)
kubectl get pod -A --sort-by=.metadata.creationTimestamp

# Sort pods by name
kubectl get pod -A --sort-by=.metadata.name

# Sort pods by uid
kubectl get pod -A --sort-by=.metadata.uid

# Sort nodes by memory capacity (descending not supported natively — pipe to sort)
kubectl get nodes --sort-by=.status.capacity.memory

# Sort events by last timestamp
kubectl get events -A --sort-by='.lastTimestamp'

# Sort PVs by capacity
kubectl get pv --sort-by=.spec.capacity.storage
```

---

## 4. `-o jsonpath`

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

## 5. `-o custom-columns`

Define your own column headers and the JSONPath for each column.

```bash
# Basic syntax
kubectl get pods -o custom-columns=COLUMN_HEADER:.json.path

# Multiple columns separated by comma
kubectl get pods -A \
  -o custom-columns=\
NAMESPACE:.metadata.namespace,\
NAME:.metadata.name,\
IMAGE:.spec.containers[0].image,\
NODE:.spec.nodeName

# Output:
# NAMESPACE    NAME         IMAGE          NODE
# default      my-pod       nginx:latest   worker-1

# Pod QoS class
kubectl get pods -A -o custom-columns=\
NAME:.metadata.name,\
QOS:.status.qosClass,\
NS:.metadata.namespace

# Nodes with internal IP
kubectl get nodes -o custom-columns=\
NAME:.metadata.name,\
STATUS:.status.conditions[-1].type,\
IP:.status.addresses[0].address

# Services with cluster IP and ports
kubectl get svc -A -o custom-columns=\
NS:.metadata.namespace,\
NAME:.metadata.name,\
CLUSTERIP:.spec.clusterIP,\
PORT:.spec.ports[0].port
```

### custom-columns from a file

```bash
# columns.txt
NAMESPACE           .metadata.namespace
NAME                .metadata.name
NODE                .spec.nodeName

kubectl get pods -A -o custom-columns-file=columns.txt
```

---

## 6. `jq` patterns

`jq` is available in most exam environments and is more powerful than JSONPath for
complex filtering.

```bash
# All pod names and their namespaces
kubectl get pods -A -o json | \
  jq '.items[] | {name:.metadata.name, ns:.metadata.namespace}'

# Pods not in Running state
kubectl get pods -A -o json | \
  jq '.items[] | select(.status.phase != "Running") | {name:.metadata.name, phase:.status.phase}'

# Container images used across the cluster
kubectl get pods -A -o json | \
  jq '[.items[].spec.containers[].image] | unique | sort[]'

# Nodes and their allocatable memory
kubectl get nodes -o json | \
  jq '.items[] | {node:.metadata.name, memory:.status.allocatable.memory}'

# Events sorted by last timestamp (jq sort)
kubectl get events -A -o json | \
  jq '[.items | sort_by(.lastTimestamp)[]] | .[] | {ns:.metadata.namespace, reason:.reason, msg:.message}'

# Find which ServiceAccounts have a given ClusterRoleBinding
kubectl get clusterrolebindings -o json | \
  jq '.items[] | select(.roleRef.name=="cluster-admin") | .subjects[]'

# Count pods per node
kubectl get pods -A -o json | \
  jq '[.items[].spec.nodeName] | group_by(.) | map({node:.[0], count:length})'
```

---

## 7. `kubectl top` — Resource Usage

`kubectl top` shows live CPU and memory consumption from **metrics-server**. If
metrics-server is not installed the command fails with `Metrics API not available`.

```bash
# Node resource usage
kubectl top node

# Example output:
# NAME       CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
# master     192m         9%     1234Mi           65%
# worker-1   88m          4%     891Mi            47%

# Pod resource usage (current namespace)
kubectl top pod

# All namespaces
kubectl top pod -A

# Specific namespace
kubectl top pod -n kube-system

# Show containers individually within each pod
kubectl top pod -A --containers

# Sort by CPU (highest first) — pipe to sort; --sort-by not supported for top
kubectl top pod -A --no-headers | sort -k3 -rn | head -10

# Sort by memory
kubectl top pod -A --no-headers | sort -k4 -rn | head -10

# Find highest CPU node
kubectl top node --no-headers | sort -k2 -rn | head -1

# Find highest memory node
kubectl top node --no-headers | sort -k4 -rn | head -1
```

### Checking if metrics-server is available

```bash
# metrics-server runs as a Deployment in kube-system
kubectl -n kube-system get deployment metrics-server

# Verify the Metrics API is registered
kubectl api-resources | grep metrics

# If missing, check the API service
kubectl get apiservice v1beta1.metrics.k8s.io -o yaml
```

### Common `kubectl top` fields

| Field | `kubectl top node` | `kubectl top pod` |
|---|---|---|
| `CPU(cores)` | millicores used by all processes | millicores used by all containers |
| `CPU%` | % of node allocatable CPU | — |
| `MEMORY(bytes)` | working set memory | working set memory |
| `MEMORY%` | % of node allocatable memory | — |

> `kubectl top` reflects the **current instant** (a scrape from metrics-server).
> For trends and history, use Prometheus + Grafana or `kubectl describe node` for
> resource request/limit totals.

---

## 8. Practical One-Liners

```bash
# Write a script that lists all pods sorted by creationTimestamp
echo 'kubectl get pod -A --sort-by=.metadata.creationTimestamp' > find_pods.sh

# Write a script that lists all pods sorted by uid
echo 'kubectl get pod -A --sort-by=.metadata.uid' > find_pods_uid.sh

# Get all container images running in the cluster (unique, sorted)
kubectl get pods -A -o jsonpath='{range .items[*]}{range .spec.containers[*]}{.image}{"\n"}{end}{end}' | \
  sort -u

# List all nodes with their OS image and kernel version
kubectl get nodes -o custom-columns=\
NAME:.metadata.name,\
OS:.status.nodeInfo.osImage,\
KERNEL:.status.nodeInfo.kernelVersion

# Check resource requests for all pods
kubectl get pods -A -o custom-columns=\
NAME:.metadata.name,\
CPU_REQ:.spec.containers[0].resources.requests.cpu,\
MEM_REQ:.spec.containers[0].resources.requests.memory

# List PVs sorted by capacity
kubectl get pv --sort-by=.spec.capacity.storage \
  -o custom-columns=\
NAME:.metadata.name,\
CAPACITY:.spec.capacity.storage,\
POLICY:.spec.persistentVolumeReclaimPolicy,\
STATUS:.status.phase

# Get events for Warning type, sorted by time
kubectl get events -A \
  --field-selector type=Warning \
  --sort-by='.lastTimestamp' \
  -o custom-columns=\
NS:.metadata.namespace,\
TIME:.lastTimestamp,\
REASON:.reason,\
OBJ:.involvedObject.name
```

---

## 9. Quick Reference Table

| Task | Command |
|---|---|
| Sort pods by age | `kubectl get pod -A --sort-by=.metadata.creationTimestamp` |
| Sort pods by UID | `kubectl get pod -A --sort-by=.metadata.uid` |
| Get pod's node | `kubectl get pod <p> -o jsonpath='{.spec.nodeName}'` |
| Get node internal IP | `kubectl get node <n> -o jsonpath='{.status.addresses[?(@.type=="InternalIP")].address}'` |
| All images in cluster | `kubectl get pods -A -o jsonpath='{range .items[*]}{.spec.containers[*].image}{"\n"}{end}'` |
| Pod restart counts | `kubectl get pod -A -o custom-columns=NAME:.metadata.name,RESTARTS:.status.containerStatuses[0].restartCount` |
| Services and ClusterIPs | `kubectl get svc -A -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name,IP:.spec.clusterIP` |
