# Question 95

> **Solve this question on:** the `cka-lab` kind cluster

The CoreDNS configuration in the cluster needs to be updated:

1. Backup the current CoreDNS `ConfigMap` to `/opt/course/16/coredns-backup.yaml`

1. Update the CoreDNS configuration so that DNS resolution for domain `very-secure.io` is forwarded to `1.2.3.4` instead of the default upstream

1. Confirm CoreDNS pods restart and the new configuration is loaded
