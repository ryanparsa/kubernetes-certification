# Question 95

> **Solve this question on:** the "cka-lab-95" kind cluster

The CoreDNS configuration in the cluster needs to be updated:

1. Backup the current CoreDNS *ConfigMap* to `/opt/course/95/coredns-backup.yaml`.

2. Update the CoreDNS configuration so that DNS resolution for domain `very-secure.io` is forwarded to `1.2.3.4` instead of the default upstream.

3. Confirm CoreDNS *Pods* restart and the new configuration is loaded.

---

**Setup:** `bash assets/setup.sh` - **Cleanup:** `bash assets/cleanup.sh`
