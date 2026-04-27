# `-o custom-columns`

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

