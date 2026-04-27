# Kubernetes Networking Reference — 6. CoreDNS

> Part of [Kubernetes Networking Reference](../Networking Reference.md)


CoreDNS runs as a Deployment in `kube-system`, exposed via the `kube-dns` Service at
the cluster DNS IP (usually `10.96.0.10`).

```bash
# Find the DNS service IP
kubectl -n kube-system get svc kube-dns

# Check CoreDNS pods
kubectl -n kube-system get pods -l k8s-app=kube-dns

# View CoreDNS config
kubectl -n kube-system get configmap coredns -o yaml
```

### CoreDNS ConfigMap (Corefile)

```
.:53 {
    errors
    health {       lameduck 5s }
    ready
    kubernetes cluster.local in-addr.arpa ip6.arpa {
       pods insecure
       fallthrough in-addr.arpa ip6.arpa
       ttl 30
    }
    prometheus :9153
    forward . /etc/resolv.conf {
       max_concurrent 1000
    }
    cache 30
    loop
    reload
    loadbalance
}
```

### Adding a custom upstream DNS (stub zone)

```
my-corp.internal:53 {
    errors
    cache 30
    forward . 192.168.1.1
}
```

Add the block to the Corefile in the ConfigMap and restart CoreDNS pods:

```bash
kubectl -n kube-system rollout restart deployment coredns
```

---

