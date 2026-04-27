## Answer

### How many controlplane and worker *Nodes* are available?

```bash
kubectl get node
NAME                     STATUS   ROLES           AGE   VERSION
cka-lab-31-control-plane   Ready    control-plane   71m   v1.33.1
```

We see one controlplane and no worker *Nodes*.

### What is the *Service* CIDR?

Access the control-plane *Node* to inspect the *kube-apiserver* manifest:

```bash
docker exec cka-lab-31-control-plane cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep range
    - --service-cluster-ip-range=10.96.0.0/12
```

### Which Networking (or CNI Plugin) is configured and where is its config file?

```bash
docker exec cka-lab-31-control-plane find /etc/cni/net.d/
/etc/cni/net.d/
/etc/cni/net.d/10-kindnet.conflist
```

In kind clusters, the default CNI plugin is **kindnet**. The config file is at `/etc/cni/net.d/10-kindnet.conflist`.

> [!NOTE]
> In the real exam environment, a different CNI (such as Weave or Flannel) may be configured. The approach is the same: look in `/etc/cni/net.d/` on the *Node*.

### Which suffix will static *Pods* have that run on cka-lab-31-control-plane?

The suffix is the *Node* hostname with a leading hyphen.

### Result

The resulting `cka/31/lab/cluster-info` could look like:

```
# cka/31/lab/cluster-info

# How many controlplane *Nodes* are available?
1: 1

# How many worker *Nodes* (non controlplane *Nodes*) are available?
2: 0

# What is the *Service* CIDR?
3: 10.96.0.0/12

# Which Networking (or CNI Plugin) is configured and where is its config file?
4: kindnet, /etc/cni/net.d/10-kindnet.conflist

# Which suffix will static *Pods* have that run on cka-lab-31-control-plane?
5: -cka-lab-31-control-plane
```


## Killer.sh Checklist (Score: 0/5)

- [ ] Answer 1 valid
- [ ] Answer 2 valid
- [ ] Answer 3 valid
- [ ] Answer 4 valid
- [ ] Answer 5 valid
