## Answer

**Reference:** https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/

### 1. Backup CoreDNS *ConfigMap*

```bash
# On the control-plane node
kubectl -n kube-system get cm coredns -o yaml > /opt/course/95/coredns-backup.yaml
```

### 2. Update CoreDNS *ConfigMap*

Edit the *ConfigMap*:
```bash
kubectl -n kube-system edit cm coredns
```

Add the following block to the `Corefile` data:

```yaml
very-secure.io:53 {
    forward . 1.2.3.4
}
```

Example of updated `Corefile`:
```text
.:53 {
    errors
    health {
       lameduck 5s
    }
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
very-secure.io:53 {
    forward . 1.2.3.4
}
```

### 3. Restart CoreDNS *Pods*

Restart the deployment to pick up the changes immediately:
```bash
kubectl -n kube-system rollout restart deployment coredns
```

Verify the rollout:
```bash
kubectl -n kube-system rollout status deployment coredns
```

## Checklist (Score: 0/3)

- [ ] CoreDNS *ConfigMap* backed up to `/opt/course/95/coredns-backup.yaml`
- [ ] CoreDNS configured to forward `very-secure.io` to `1.2.3.4`
- [ ] CoreDNS *Pods* restarted and running with new configuration
