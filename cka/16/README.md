# Question 16

> **Solve this question on:** the `cka-lab` kind cluster

The CoreDNS configuration in the cluster needs to be updated:

1. Make a backup of the existing configuration YAML and store it at `cka/16/lab/coredns_backup.yaml`. You should be able to fast recover from the backup.
2. Update the CoreDNS configuration in the cluster so that DNS resolution for `SERVICE.NAMESPACE.custom-domain` will work exactly like and in addition to `SERVICE.NAMESPACE.cluster.local`.

Test your configuration for example from a *Pod* with `busybox:1` image. These commands should result in an IP address:

```
nslookup kubernetes.default.svc.cluster.local
nslookup kubernetes.default.svc.custom-domain
```

---

**Setup:** `bash assets/setup.sh` · **Cleanup:** `bash assets/cleanup.sh`
