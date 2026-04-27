# Kubernetes Networking Reference — 7. kube-proxy

> Part of [Kubernetes Networking Reference](../Networking Reference.md)


kube-proxy runs as a DaemonSet on every node and implements Service VIP routing.

### Modes

| Mode | Mechanism | Notes |
|---|---|---|
| `iptables` (default) | iptables DNAT rules | Stable, random load-balancing |
| `ipvs` | Linux IPVS | Better performance at scale, more LB algorithms |
| `nftables` | nftables (Kubernetes 1.29+) | Modern replacement for iptables mode |

```bash
# Check current mode
kubectl -n kube-system get configmap kube-proxy -o yaml | grep mode

# Inspect iptables rules for a Service
iptables-save | grep <service-cluster-ip>

# Inspect IPVS virtual servers (if IPVS mode)
ipvsadm -Ln
```

---

