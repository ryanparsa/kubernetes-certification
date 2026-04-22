# Question 14 | Find out Cluster Information

You're ask to find out following information about the cluster:

1. How many controlplane nodes are available?
2. How many worker nodes (non controlplane nodes) are available?
3. What is the Service CIDR?
4. Which Networking (or CNI Plugin) is configured and where is its config file?
5. Which suffix will static pods have that run on `cka-lab-control-plane`?

Write your answers into file `cka/31/course/cluster-info`, structured like this:

```
# cka/31/course/cluster-info
1: [ANSWER]
2: [ANSWER]
3: [ANSWER]
4: [ANSWER]
5: [ANSWER]
```

## Answer

### How many controlplane and worker nodes are available?

```bash
k get node
NAME                    STATUS   ROLES           AGE   VERSION
cka-lab-control-plane   Ready    control-plane   71m   v1.33.1
```

We see one controlplane and no worker nodes.

### What is the Service CIDR?

Access the control-plane node to inspect the kube-apiserver manifest:

```bash
docker exec cka-lab-control-plane cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep range
    - --service-cluster-ip-range=10.96.0.0/12
```

### Which Networking (or CNI Plugin) is configured and where is its config file?

```bash
docker exec cka-lab-control-plane find /etc/cni/net.d/
/etc/cni/net.d/
/etc/cni/net.d/10-kindnet.conflist
```

In kind clusters, the default CNI plugin is **kindnet**. The config file is at `/etc/cni/net.d/10-kindnet.conflist`.

> [!NOTE]
> In the real exam environment, a different CNI (such as Weave or Flannel) may be configured. The approach is the same: look in `/etc/cni/net.d/` on the node.

### Which suffix will static pods have that run on cka-lab-control-plane?

The suffix is the node hostname with a leading hyphen.

### Result

The resulting `cka/31/course/cluster-info` could look like:

```
# cka/31/course/cluster-info

# How many controlplane nodes are available?
1: 1

# How many worker nodes (non controlplane nodes) are available?
2: 0

# What is the Service CIDR?
3: 10.96.0.0/12

# Which Networking (or CNI Plugin) is configured and where is its config file?
4: kindnet, /etc/cni/net.d/10-kindnet.conflist

# Which suffix will static pods have that run on cka-lab-control-plane?
5: -cka-lab-control-plane
```
