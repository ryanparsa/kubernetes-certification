# Question 195

> **Solve this question on:** `ssh cka4774`

The CoreDNS configuration in the cluster needs to be updated:

1. Make a backup of the existing CoreDNS configuration and store it at `/opt/course/16/coredns_backup.yaml`

1. Update the CoreDNS configuration in the cluster so that DNS resolution for `SERVICE.NAMESPACE.cluster-domain` will work exactly like — and in addition to — `SERVICE.NAMESPACE.cluster.local`

Test your configuration from a Pod with `busybox:1` image. These commands should both return an IP address:

```bash
nslookup kubernetes.default.svc.cluster.local
nslookup kubernetes.default.svc.cluster-domain
```
