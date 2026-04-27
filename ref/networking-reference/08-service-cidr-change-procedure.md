# Kubernetes Networking Reference — 8. Service CIDR Change Procedure

> Part of [Kubernetes Networking Reference](../Networking Reference.md)


Changing the Service CIDR after cluster creation requires updating multiple components.

### Steps (kubeadm cluster)

```bash
# 1. Update kube-apiserver static pod manifest
vim /etc/kubernetes/manifests/kube-apiserver.yaml
# Change: --service-cluster-ip-range=NEW_CIDR

# 2. Update kube-controller-manager static pod manifest
vim /etc/kubernetes/manifests/kube-controller-manager.yaml
# Change: --service-cluster-ip-range=NEW_CIDR

# 3. Update kube-proxy configmap
kubectl -n kube-system edit configmap kube-proxy
# Change clusterCIDR or the iptables/ipvs config

# 4. Update CoreDNS Service (kube-dns) IP if needed
# Delete the kube-dns Service so it gets a new IP from the new CIDR
kubectl -n kube-system delete svc kube-dns
# Re-create it with an explicit IP from the new CIDR:
kubectl -n kube-system expose deployment coredns \
  --name=kube-dns \
  --port=53 \
  --protocol=UDP \
  --cluster-ip=NEW_DNS_IP

# 5. Update kubelet's clusterDNS setting on each node
# Edit /var/lib/kubelet/config.yaml:
# clusterDNS:
# - NEW_DNS_IP
# Then restart kubelet: systemctl restart kubelet

# 6. Restart affected pods so they pick up the new /etc/resolv.conf
# Recreate kube-proxy DaemonSet pods
kubectl -n kube-system rollout restart daemonset kube-proxy
```

> All existing Services retain their old ClusterIPs until deleted and re-created.
> The `kubernetes` Service in the `default` Namespace must also be deleted and re-created.

---

